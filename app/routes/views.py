import os
import tarfile
import zipfile
import json
import redis
from datetime import datetime
# flask/external lib
from flask import Blueprint, render_template, request, jsonify, current_app, g, url_for, redirect
from rq import Queue
from werkzeug.utils import secure_filename
from flask_recaptcha import ReCaptcha
# spfy code
from modules.spfy import spfy
from routes.utility_functions import handle_tar, handle_zip, fix_uri
from modules.groupComparisons.frontend_queries import get_all_attribute_types, get_attribute_values, get_types
bp = Blueprint('main', __name__)
from modules.gc import blob_gc_enqueue

@bp.route('/api/v0/results/<job_id>')
def job_status_reactapp(job_id):
    '''
    This provides an endpoint for the reactapp to poll results. We leave job_status() intact to maintain backwards compatibility with the AngularJS app.
    '''
    job = fetch_job(job_id)
    if job.is_finished:
        return job.result
    elif job.is_failed:
        return job.exc_info, 415
    else:
        return "pending", 204

@bp.route('/api/v0/newgroupcomparison', methods=['POST'])
def handle_group_comparison_submission():
    query = request.json['groups']
    target = request.json['target']
    jobid = blob_gc_enqueue(query, target)
    return jobid

@bp.route('/api/v0/get_attribute_values/type/<path:attributetype>')
def call_get_attribute_values(attributetype):
    '''
    Front-End API:
    Get all attribute values for a given attribute type.
    '''
    # workaround: Flask's path converter allows slashes, but only a SINGLE slash
    # this adds the second slash
    # also convert to a rdflib.URIRef object
    uri = fix_uri(attributetype)
    return jsonify(get_attribute_values(attributeTypeUri=uri))
    # set_attribute_types = set(get_all_attribute_types())
    # set_object_types = get_types() # get types returns a set by default
    # return jsonify(list(set_attribute_types.union(set_object_types)))

@bp.route('/api/v0/get_all_types')
def combine_types():
    '''
    Returns all URIs that is either a attribute type or and object type.
    '''
    set_attribute_types = set(get_all_attribute_types())
    set_object_types = get_types() # get types returns a set by default
    return jsonify(list(set_attribute_types.union(set_object_types)))

@bp.route('/api/v0/get_all_attribute_types')
def call_get_all_atribute_types():
    '''
    Front-End API:
    Get all possible attribute types.
    '''
    return jsonify(get_all_attribute_types())

def fetch_job(job_id):
    '''
    Iterates through all queues looking for the job.
    '''
    redis_url = current_app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    queues = current_app.config['QUEUES_SPFY']
    for queue in queues:
        q = Queue(queue, connection=redis_connection)
        job = q.fetch_job(job_id)
        if job is not None:
            return job
    return {'is_failed': True, 'exc_info': 'job not found'}

@bp.route('/results/<job_id>')
def job_status(job_id):
    job = fetch_job(job_id)
    if job.is_finished:
        return jsonify(job.result)
    elif job.is_failed:
        return job.exc_info, 415
    else:
        return "Still pending", 202

@bp.route('/upload', methods=['POST'])
def upload():
    recaptcha = ReCaptcha(app=current_app)
    if recaptcha.verify():
        form = request.form
        options = {}
        #defaults
        options['amr']=True
        options['vf']=True
        options['serotype']=True
        options['pi']=90

        # processing form data
        for key, value in form.items():
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

        # get a list of files submitted
        uploaded_files = request.files.getlist("file")
        print uploaded_files

        #set up constants for identifying this sessions
        now = datetime.now()
        now = now.strftime("%Y-%m-%d-%H-%M-%S-%f")
        jobs_dict = {}

        for file in uploaded_files:
            if file:
                # for saving file
                filename = os.path.join(current_app.config[
                                        'DATASTORE'], now + '-' + secure_filename(file.filename))
                file.save(filename)
                print 'IVE SAVED YO FILE AT', str(filename)

                if tarfile.is_tarfile(filename):
                    # set filename to dir for spfy call
                    filename = handle_tar(filename, now)
                elif zipfile.is_zipfile(filename):
                    filename = handle_zip(filename, now)

                # for enqueing task
                jobs_enqueued = spfy(
                    {'i': filename, 'disable_serotype': False, 'disable_amr': False, 'disable_vf': False, 'pi':options['pi'], 'options':options})
                jobs_dict.update(jobs_enqueued)
        return jsonify(jobs_dict)
    else:
        return "Captcha Failed Verification", 500

@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")
