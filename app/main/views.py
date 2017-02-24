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
        form = request.form
        options = {}
        #defaults
        options['amr']=True
        options['vf']=True
        options['serotype']=True
        options['pi']=90

        print "=== Form Data ==="
        for key, value in form.items():
            print key, '==>', value
            #we need to convert lower-case true/false in js to upper case in python
                #remember, we also have numbers
            if not value.isdigit():
                if value.lower() == 'false':
                    value = False
                else:
                    value = True
                if key == 'options.amr':
                    options['amr']=value
                if key == 'options.vf':
                    options['vf']=value
                if key == 'options.serotype':
                    options['serotype']=value
            else:
                if key =='options.pi':
                    options['pi']=int(value)

        file = request.files['file']
        if file:
            # for saving file
            now = datetime.now()
            now = now.strftime("%Y-%m-%d-%H-%M-%S-%f")

            filename = os.path.join(current_app.config[
                                    'UPLOAD_FOLDER'], now + '-' + secure_filename(file.filename))
            file.save(filename)

            if tarfile.is_tarfile(filename):
                # set filename to dir for spfy call
                filename = handle_tar(filename, now)

            # for enqueing task
            jobs_dict = spfy.spfy(
                {'i': filename, 'disable_serotype': not options['serotype'], 'disable_amr': not options['amr'], 'disable_vf': not options['vf'], 'pi':options[pi]})

            print jobs_dict
            #strip jobs that the user doesn't want to see
            # we run them anyways cause we want the data analyzed on our end
            for job_id, descrip_dict in jobs_dict.items():
                print job_id, descrip_dict
                print options
                if (not options['serotype']) and (not options['vf']):
                    if descrip_dict['analysis'] == 'Virulence Factors and Serotype':
                        print 'deleteing s/vf'
                        del jobs_dict[job_id]
                if (not options['amr']):
                    print 'in amr del'
                    if descrip_dict['analysis'] == 'Antimicrobial Resistance':
                        print 'deleting amr'
                        del jobs_dict[job_id]

            return jsonify(jobs_dict)
    return 500


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

def handle_tar(filename, now):
    if tarfile.is_tarfile(filename):
        tar = tarfile.open(filename)
        extracted_dir = os.path.join(
            current_app.config['UPLOAD_FOLDER'] + '/' + now)
        os.mkdir(extracted_dir)
        for member in tar.getmembers():
            if not secure_filename(member.name):
                return 'invalid upload', 500
                # TODO: wipe temp data
        tar.extractall(path=extracted_dir)
        for fn in os.listdir(extracted_dir):
            os.rename(extracted_dir +'/' + fn, extracted_dir +'/'+ now + '-' + fn)
        tar.close()

        # set filename to dir for spfy call
        return extracted_dir
