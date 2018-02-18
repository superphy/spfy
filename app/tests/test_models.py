from middleware.models import SubtypingRow, SubtypingResult, Pipeline, Job
from modules.spfy import spfy
from scripts.savvy import savvy
from tests.constants import BEAUTIFY_VF_SEROTYPE, ARGS_DICT


def test_subtyping_model_direct():
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
    for d in BEAUTIFY_VF_SEROTYPE]
    subtyping_result = SubtypingResult(
        rows = subtyping_list
    )
    subtyping_result.validate()

def test_pipeline_model():
    """
    Test the Pipeline model itself.
    """
    p = Pipeline(
        func = spfy,
        options = ARGS_DICT
    )
    pipeline.jobs.update({
        'job_ectyper_vf': Job(
            rq_job='SHOULDBEANACTUALJOB',
            name='job_ectyper_vf',
            transitory=True,
            backlog=False,
            display=False
        )
    })
    assert isinstance(p, Pipeline)
    assert isinstance(p.jobs, dict)
    assert isinstance(p.jobs['job_ectyper_vf'], Job)


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
