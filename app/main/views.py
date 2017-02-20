import os
import tarfile
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
    print 'received'
    print job_id
    for queue in current_app.config['QUEUES']:
        q = Queue(queue, connection=Redis())
        job = q.fetch_job(job_id)
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
        if file:
            # for saving file
            now = datetime.now()
            now = now.strftime("%Y-%m-%d-%H-%M-%S-%f")

            filename = os.path.join(current_app.config['UPLOAD_FOLDER'], now + '-' + secure_filename(file.filename))
            file.save(filename)

            if tarfile.is_tarfile(filename):
                tar = tarfile.open(filename)
                extracted_dir = os.path.join(current_app.config['UPLOAD_FOLDER'] + '/' + now)
                os.mkdir(extracted_dir)
                for member in tar.getmembers():
                    if not secure_filename(member.name):
                        return 'invalid upload', 500
                        #TODO: wipe temp data
                tar.extractall(path=extracted_dir)
                tar.close()

                #set filename to dir for spfy call
                # tar.extractall will create a another folder at targer directory under filename
                #edge case .tar.gz
                s = file.filename
                if '.tar.gz' in filename:
                    filename = extracted_dir + '/' + s.strip('.tar.gz')
                else:
                    filename = d + '/' + os.path.splitext(s)[0]

                print 'filename in if is ' + filename

            print 'filename before call is' + filename
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
