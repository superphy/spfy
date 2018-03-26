import redis

from flask import Blueprint, jsonify, current_app
from routes.job_utils import fetch_job

bp_ra_timings = Blueprint('reactapp_timings', __name__)

@bp_ra_timings.route('/api/v0/timings/<job_id>')
def job_timings(job_id):
    # Start a redis connection.
    redis_url = current_app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)

    job = fetch_job(job_id, redis_connection)
    assert job.is_finished

    start = job.started_at
    stop = job.ended_at
    timedelta = stop - start
    return jsonify(str(timedelta))
