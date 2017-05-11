import redis
import config
from rq import Queue
from modules.groupComparisons.groupcomparisons import groupcomparisons

redis_url = config.REDIS_URL
redis_conn = redis.from_url(redis_url)
multiples_q = Queue('multiples', connection=redis_conn, default_timeout=600)

def blob_gc_enqueue(query, target):
    job_gc = multiples_q.enqueue(groupcomparisons, query, target)
    print 'JOB ID IS: ' + job_gc.get_id()
