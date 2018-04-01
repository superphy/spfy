import redis
import config

from flask import Blueprint, jsonify
from routes.job_utils import fetch_job
from middleware.models import load, Pipeline

bp_ra_timings = Blueprint('reactapp_timings', __name__)

def _time_pipeline(pipeline_id):
    '''Return timings from a Pipeline instance
    '''
    # Retrieve the models.Pipeline instance.
    pipeline = load(pipeline_id)
    assert isinstance(pipeline, Pipeline)
    return pipeline.timings()

def _time_direct(job_id):
    '''Return timing from a single RQ job
    '''
    # Start a Redis connection.
    redis_url = config.REDIS_URL
    redis_connection = redis.from_url(redis_url)

    job = fetch_job(job_id, redis_connection)
    assert job.is_finished

    start = job.started_at
    stop = job.ended_at
    timedelta = stop - start
    return timedelta.total_seconds()

@bp_ra_timings.route('/api/v0/timings/<job_id>')
def job_timings(job_id):
    if job_id.startswith('pipeline'):
        return jsonify(_time_pipeline(job_id))
    else:
        return jsonify(_time_direct(job_id))
