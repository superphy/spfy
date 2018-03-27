from fakeredis import FakeStrictRedis
from rq import Queue
from time import sleep

# async=False runs job in same thread (ie. w/o workers).
queue = Queue(async=False, connection=FakeStrictRedis())

def _mock_complete(s=0):
    sleep(s)
    return True

def _mock_failed():
    assert True == False

def test_rq_responses():
    """Tests basic responses of RQ and Job statuses.
    """
    # Setup Check.
    s = 1
    finished_job = queue.enqueue(_mock_complete, s)
    sleep(s+1)
    assert finished_job.is_finished

    # Failure Check.
    failed_job = queue.enqueue(_mock_failed)
    assert failed_job.is_failed

def test_rq_ttl_finished():
    # result_ttl Expired Check.
    s = 1
    result_ttl_job = queue.enqueue(_mock_complete,s, result_ttl=5)
    sleep(s+1)
    # Job result should still exist.
    assert result_ttl_job.is_finished
    sleep(10)
    # TODO: see what errors are thrown.
    assert result_ttl_job.is_finished == 'cats'
    assert result_ttl_job.is_failed == 'cats'
    assert result_ttl_job.result == 'cats'

def test_rq_job_stats():
    '''Check timings from RQ Jobs.
    '''
    for s in range(0,16,5):
        job = queue.enqueue(_mock_complete,s)
        start = job.started_at
        stop = job.ended_at
        assert 'start: {0}, stop: {1}'.format(start,stop) == 'cats'
