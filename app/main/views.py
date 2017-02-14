import redis
import os
import subprocess
from flask import Blueprint, render_template, request, jsonify, current_app, g, url_for, redirect
from rq import push_connection, pop_connection, Queue

from .forms import UploadForm
from .. import tasks

from werkzeug.utils import secure_filename

from datetime import datetime

bp = Blueprint('main', __name__)


def get_redis_connection():
    redis_connection = getattr(g, '_redis_connection', None)
    if redis_connection is None:
        redis_url = current_app.config['REDIS_URL']
        redis_connection = g._redis_connection = redis.from_url(redis_url)
    return redis_connection


@bp.before_request
def push_rq_connection():
    push_connection(get_redis_connection())


@bp.teardown_request
def pop_rq_connection(exception=None):
    pop_connection()


@bp.route('/status/<job_id>')
def job_status(job_id):
    q = Queue()
    job = q.fetch_job(job_id)
    if job is None:
        response = {'status': 'unknown'}
    else:
        response = {
            'status': job.get_status(),
            'result': job.result,
        }
        if job.is_failed:
            response['message'] = job.exc_info.strip().split('\n')[-1]
    return jsonify(response)


@bp.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # for saving file
            now = datetime.now()
            filename = os.path.join(current_app.config['UPLOAD_FOLDER'], "%s.%s" % (
                now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))
            file.save(filename)

            # for enqueing task
            task = request.form.get('task')
            q = Queue()
            job = q.enqueue(tasks.run, task)
            return jsonify({}), 202, {'Location': url_for('main.job_status', job_id=job.get_id())}
    return jsonify({'status': 'unknown'})


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']
