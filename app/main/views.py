import redis
import os
import subprocess
from flask import Blueprint, render_template, request, jsonify, current_app, g, url_for, redirect
from rq import push_connection, pop_connection, Queue
from rq.job import Job

from .forms import UploadForm
from .. import spfy

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


@bp.route('/results/<job_id>')
def job_status(job_id):
    job = Job.fetch(job_id, connection=conn)
    if job.is_finished:
        return jsonify(job.result)
    else:
        return "Nay!", 202


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
            job = spfy.spfy({'i':filename, 'disable_serotype':False, 'disable_amr':False,'disable_vf':False})
            print job
            return job.get_id()
    return jsonify({'success': False})


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']
