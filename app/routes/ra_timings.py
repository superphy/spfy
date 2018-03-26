from flask import Blueprint, jsonify, current_app
from routes.job_utils import fetch_job

bp_ra_timings = Blueprint('reactapp_timings', __name__)

@bp_ra_timings.route('/api/v0/timings/<job_id>')
def job_timings(job_id):
    job = fetch_job()
    assert job.is_finished

    start = job.started_at
    stop = job.ended_at
    s = start - stop
    return jsonify(s)
