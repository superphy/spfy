from fakeredis import FakeStrictRedis
from rq import Queue
from time import sleep

# async=False runs job in same thread (ie. w/o workers).
queue = Queue(async=False, connection=FakeStrictRedis())

def _mock_complete(s=0):
    sleep(s)
    return 'cats'

def test_rq_responses():
    """Tests basic responses of RQ and Job statuses.
    """
    # Setup Check.
    s = 1
    finished_job = queue.enqueue(_mock_complete, s)
    sleep(s+1)
    assert finished_job.is_finished

def test_rq_ttl_finished():
    # result_ttl Expired Check.
    s = 1
    result_ttl_job = queue.enqueue(_mock_complete,s, result_ttl=5)
    sleep(s+1)
    # Job result should still exist.
    assert result_ttl_job.is_finished
    sleep(10)
    # Check various job statuses.
    assert result_ttl_job.is_finished == True
    assert result_ttl_job.is_failed == False
    assert result_ttl_job.result == 'cats'
