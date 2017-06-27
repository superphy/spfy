import logging
import config
import redis
from rq import Queue
from modules.groupComparisons.groupcomparisons import groupcomparisons
from modules.loggingFunctions import initialize_logging
from modules.decorators import tofromHumanReadable

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

redis_url = config.REDIS_URL
redis_conn = redis.from_url(redis_url)
multiples_q = Queue('multiples', connection=redis_conn, default_timeout=600)

@tofromHumanReadable
def convert(q):
    """
    Used to convert the human-readable string back into a proper URI.
    """
    return q

def blob_gc_enqueue(query, target):
    job_gc = multiples_q.enqueue(groupcomparisons, convert(query), convert(target), result_ttl=-1)
    log.info('JOB ID IS: ' + job_gc.get_id())
    return job_gc.get_id()
