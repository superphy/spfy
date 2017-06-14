import redis
from flask import current_app
from rq import Queue

def fetch_job(job_id):
    '''
    Iterates through all queues looking for the job.
    '''
    redis_url = current_app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    queues = current_app.config['QUEUES_SPFY']
    for queue in queues:
        q = Queue(queue, connection=redis_connection)
        job = q.fetch_job(job_id)
        if job is not None:
            return job
    print 'fetch_job(): ERROR ' + job_id + ' not found'
    return Job(is_failed=True, exc_info='job not found')

class Job(object):
    '''
    A class to mimick the Job object returned by RQ's Queue.fetch_job()
    We use this to create custom Jobs with our own error messages.
    This allows custom error messages to be parsed by the same code.
    '''
    def __init__(self, is_finished=False, result='', is_failed=False, exc_info=''):
        self.is_finished = is_finished
        self.result = result
        self.is_failed = is_failed
        self.exc_info = exc_info
