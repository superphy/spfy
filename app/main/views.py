import os
from flask import Blueprint, render_template, request, jsonify, current_app, g, url_for, redirect
from rq import Queue
from redis import Redis

from .forms import UploadForm
from .. import spfy

from werkzeug.utils import secure_filename

from datetime import datetime

bp = Blueprint('main', __name__)

def fetch_job(job_id):
    '''
    Iterates through all queues looking for the job.
    '''
    for queue in current_app.config['QUEUES']:
        q = Queue(queue,connection=Redis())
        job = q.fetch_job(job_id)
        #debugging
        print job
        if job is not None:
            return job

@bp.route('/results/<job_id>')
def job_status(job_id):
    job = fetch_job(job_id)
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
            jobs_dict = spfy.spfy(
                {'i': filename, 'disable_serotype': False, 'disable_amr': False, 'disable_vf': False})
            print jobs_dict
            return jsonify(jobs_dict)
    return 500


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']
