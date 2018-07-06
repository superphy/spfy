import dill
from middleware import models, modellers
from modules.spfy import spfy
from scripts.savvy import savvy
from tests import constants
from tests.test_modules import test_ectyper_vf, test_ectyper_serotype_call_pickle

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

def test_subtyping_model_direct(l=constants.BEAUTIFY_VF_SEROTYPE):
    """
    Use our dataset to directly create a subtyping results model and validate it.
    """
    subtyping_list = modellers.model_vf(l)
    # Return for incorporation into later tests.
    return subtyping_list

def _create_example_pipeline():
    p = models.Pipeline(
        func=spfy,
        options=constants.ARGS_DICT
    )
    r_serotype = test_ectyper_serotype_call_pickle(return_one=True)
    mock_serotype = MockRQJob(
        result=test_subtyping_model_direct(r_serotype)
    )
    r_vf = test_ectyper_vf(return_one=True)
    mock_vf = MockRQJob(
        result=test_subtyping_model_direct(r_vf)
    )
    # Mimicks a Serotype result that will be converted to json.
    p.jobs.update({
        'job_ectyper_beautify_serotype': models.Job(
            rq_job=mock_serotype,
            name='job_ectyper_beautify_vf',
            transitory=False,
            backlog=False,
            display=True
        )
    })
    # Mimicks a VF result that will be converted to json.
    p.jobs.update({
        'job_ectyper_beautify_vf': models.Job(
            rq_job=mock_vf,
            name='job_ectyper_beautify_vf',
            transitory=False,
            backlog=False,
            display=True
        )
    })
    return p

def test_pipeline_model_subtyping(p=None):
    """
    Test the Pipeline model itself for subtyping via ECTyper and RGI.
    """
    if not p:
        p = _create_example_pipeline()

    assert isinstance(p, models.Pipeline)
    assert isinstance(p.jobs, dict)
    for k in p.jobs:
        assert isinstance(p.jobs[k], models.Job)

    # Test Pipeline.cache_jobs()
    p.cache_jobs('somefilename.fasta')
    # Test Pipeline.merge_jobs()
    p.merge_jobs()

def test_pipeline_model_dill():
    p = _create_example_pipeline()
    # Test dumping the Pipeline into a str.
    buffer = dill.dumps(p)
    # Test loading the Pipeline from a str.
    loaded_pipeline = dill.loads(buffer)
    # Run the same tests on the loaded pipeline.
    test_pipeline_model_subtyping(p=loaded_pipeline)

# def test_pipeline_model_phyotyping():
#     """
#     Test the Pipeline model itself for subtyping via Phylotyper.
#     """
#     p = models.Pipeline(
#         func = spfy,
#         options = constants.ARGS_DICT
#     )
#     mock_stx1 = MockRQJob(
#         result = test_phylotyper_model_direct(constants.BEAUTIFY_STX1)
#     )
#     mock_stx2 = MockRQJob(
#         result = test_phylotyper_model_direct(constants.BEAUTIFY_STX2)
#     )
#     p.jobs.update({
#         'job_phylotyper_beautify_stx1': models.Job(
#             rq_job=mock_stx1,
#             name='job_phylotyper_beautify_stx1',
#             transitory=False,
#             backlog=False,
#             display=True
#         )
#     })
#     p.jobs.update({
#         'job_phylotyper_beautify_stx2': models.Job(
#             rq_job=mock_stx2,
#             name='job_phylotyper_beautify_stx2',
#             transitory=False,
#             backlog=False,
#             display=True
#         )
#     })
#     assert isinstance(p, models.Pipeline)
#     assert isinstance(p.jobs, dict)
#     for k in p.jobs:
#         assert isinstance(p.jobs[k], models.Job)
#
#     # Test Pipeline.cache_jobs()
#     p.cache_jobs()
#     # Test Pipeline.merge_jobs()
#     p.merge_jobs()
#     # Test Pipeline.complete(), should be True.
#     assert p.complete()
#
#     # Test Pipeline.to_json().
#     json = p.to_json()
#     assert isinstance(json, list)
#
#     # Add an AMR job and re-test.
#     mock_eae  = MockRQJob(
#         result = test_phylotyper_model_direct(constants.BEAUTIFY_EAE)
#     )
#     p.jobs.update({
#         'job_phylotyper_beautify_eae': models.Job(
#             rq_job=mock_eae,
#             name='job_phylotyper_beautify_stx2',
#             transitory=False,
#             backlog=False,
#             display=True
#         )
#     })
#     p.merge_jobs()
#     # Test Pipeline.complete(), should be True.
#     assert p.complete()
#     # Test Pipeline.to_json().
#     json = p.to_json()
#     assert isinstance(json, list)

def test_pipeline_model_signature():
    """
    Function signatures should be identical if called on the same function.
    """
    p1 = models.Pipeline(
        func = spfy,
        options = constants.ARGS_DICT
    )
    p2 = models.Pipeline(
        func = spfy,
        options = constants.ARGS_DICT
    )
    # Signatures should be generated on init.
    assert p1.sig == p2.sig

    # Call the signature method to re-generate.
    r1 = p1.signature()
    r2 = p2.signature()
    # These are identical pipelines, should be equal.
    assert r1 == r2

    # Both methods of signature generation should be the same.
    assert p1.sig == r1
    assert p2.sig == r2

    p1 = models.Pipeline(
        func = spfy,
        options = constants.ARGS_DICT
    )
    p2 = models.Pipeline(
        func = savvy,
        options = constants.ARGS_DICT
    )
    r1 = p1.signature()
    r2 = p2.signature()
    # These pipelines have different functions, should be different.
    assert r1 != r2

    p1 = models.Pipeline(
        func = spfy,
        options = constants.ARGS_DICT
    )
    p2 = models.Pipeline(
        func = spfy,
        options = {'cats':1}
    )
    r1 = p1.signature()
    r2 = p2.signature()
    # These pipelines have different options, should be different.
    assert r1 != r2
