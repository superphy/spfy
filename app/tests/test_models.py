from middleware.models import SubtypingRow, SubtypingResult, Pipeline, Job
from modules.spfy import spfy
from scripts.savvy import savvy
from tests.constants import BEAUTIFY_VF_SEROTYPE, BEAUTIFY_SEROTYPE, BEAUTIFY_VF, ARGS_DICT

class MockRQJob():
    """
    A mock Job class returned by RQ. Also emulates response the Job gets from
    querying Redis DB.
    """
    def __init__(self, is_finished=True, is_failed=False, exc_info='', result=None):
        self.is_finished = is_finished
        self.is_failed = is_failed
        self.exc_info = exc_info
        self.result = result

def test_subtyping_model_direct(l=BEAUTIFY_VF_SEROTYPE):
    """
    Use our dataset to directly create a subtyping results model and validate it.
    """
    subtyping_list = [
        SubtypingRow(
            analysis=d['analysis'],
            contigid=d['contigid'],
            filename=d['filename'],
            hitcutoff=str(d['hitcutoff']),
            hitname=d['hitname'],
            hitorientation=d['hitorientation'],
            hitstart=str(d['hitstart']),
            hitstop=str(d['hitstop'])
        )
    for d in l]
    subtyping_result = SubtypingResult(
        rows = subtyping_list
    )
    subtyping_result.validate()
    # Return for incorporation into later tests.
    return subtyping_result

def test_pipeline_model():
    """
    Test the Pipeline model itself.
    """
    p = Pipeline(
        func = spfy,
        options = ARGS_DICT
    )
    mock_serotype = MockRQJob(
        result = test_subtyping_model_direct(BEAUTIFY_SEROTYPE)
    )
    mock_vf = MockRQJob(
        result = test_subtyping_model_direct(BEAUTIFY_VF)
    )
    # Mimicks a Serotype result that will be converted to json.
    p.jobs.update({
        'job_ectyper_beautify_serotype': Job(
            rq_job=mock_serotype,
            name='job_ectyper_beautify_vf',
            transitory=False,
            backlog=False,
            display=True
        )
    })
    # Mimicks a VF result that will be converted to json.
    p.jobs.update({
        'job_ectyper_beautify_vf': Job(
            rq_job=mock_vf,
            name='job_ectyper_beautify_vf',
            transitory=False,
            backlog=False,
            display=True
        )
    })
    assert isinstance(p, Pipeline)
    assert isinstance(p.jobs, dict)
    for k in p.jobs:
        assert isinstance(p.jobs[k], Job)

    # Test Pipeline.complete(), should be True.
    assert p.complete()

    # Test Pipeline.to_json().
    json = p.to_json()
    assert isinstance(json, list)

def test_pipeline_model_signature():
    """
    Function signatures should be identical if called on the same function.
    """
    p1 = Pipeline(
        func = spfy,
        options = ARGS_DICT
    )
    p2 = Pipeline(
        func = spfy,
        options = ARGS_DICT
    )
    r1 = p1.signature()
    r2 = p2.signature()
    # These are identical pipelines, should be equal.
    assert r1 == r2

    p1 = Pipeline(
        func = spfy,
        options = ARGS_DICT
    )
    p2 = Pipeline(
        func = savvy,
        options = ARGS_DICT
    )
    r1 = p1.signature()
    r2 = p2.signature()
    # These pipelines have different functions, should be different.
    assert r1 != r2

    p1 = Pipeline(
        func = spfy,
        options = ARGS_DICT
    )
    p2 = Pipeline(
        func = spfy,
        options = {'cats':1}
    )
    r1 = p1.signature()
    r2 = p2.signature()
    # These pipelines have different options, should be different.
    assert r1 != r2
