import os
import tarfile
import zipfile
import redis
from flask import Blueprint, request, jsonify, current_app
from flask_recaptcha import ReCaptcha
from datetime import datetime
from werkzeug.utils import secure_filename
from ast import literal_eval
from modules.groupComparisons.frontend_queries import get_all_attribute_types, get_attribute_values, get_types
from routes.utility_functions import fetch_job, fix_uri, handle_tar, handle_zip
from modules.gc import blob_gc_enqueue
from modules.spfy import spfy

bp_ra = Blueprint('reactapp', __name__)


def handle_groupresults(jobs_dict):
    '''
    if we're grouping results for the Front-End
    take all jobs in jobs_dict and store it in Redis (not RQ)
    respond with a key to fetch this jobs_dict from Redis
    relies on a new check in /results/<job_id> which is able to poll RQ
    tasks on behalf of the front-end
        Args:
            jobs_dict (dict): a dictionary where job ids are the keys and
                the values are also dictionaries with keys 'analysis' and 'file'
        Return:
            (dict): a dictionary with key as novel jobid of form 'blob' + hash
                meant to be parsable by same code as for old, non-grouped ver
    '''
    # generate a novel job id
    # we prepend 'blob' so the /results path can tell its our custom object
    # and shouldnt be retrieved from RQ
    job_id = 'blob' + str(hash(str(jobs_dict)))
    # start a redis connection
    redis_url = current_app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    #with redis.from_url(redis_url) as redis_connection:
    # set the job_id: jobs_dict pair in Redis
    redis_connection.set(job_id, jobs_dict)
    # create a similar structure to the old return
    d = {}
    d[job_id] = {}
    d[job_id]['analysis'] = "Subtyping"
    st = set()
    for key in jobs_dict:
        st.add(jobs_dict[key]['file'])
    s = ''
    for f in st:
        s += f + ' '
    d[job_id]['file'] = s
    return d

# the /api/v0 prefix is set to allow CORS for any postfix
# this is a modification of the old upload() methods in views.py
@bp_ra.route('/api/v0/upload', methods=['POST'])
def upload():
    recaptcha = ReCaptcha(app=current_app)
    if recaptcha.verify():
        form = request.form
        options = {}
        # defaults
        options['amr']=True
        options['vf']=True
        options['serotype']=True
        options['pi']=90
        # new to 4.2.0
        # we consider False as default as the front-end should override this
        # to use the new feature
        groupresults = False

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
                if key == 'options.groupresults':
                    groupresults = value
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
        # new in 4.2.0
        if groupresults:
            return jsonify(handle_groupresults(jobs_dict))
        else:
            return jsonify(jobs_dict)
    else:
        return "Captcha Failed Verification", 500

# new to 4.2.0
def merge_job_results(jobs_dict):
    '''
    Appends all results together and returns it.
    We don't do this while retriving job statuses as in most checks, the jobs
    wont all be finished
    Note: written for lists atm. (ie. only for Subtyping)
    '''
    r = []
    for key in jobs_dict:
        job = fetch_job(key)
        if job.is_finished:
            res = job.result
            # we check for type of result as we're not returning
            # Quality Control or ID Reservation results
            # print type(res)
            if type(res) is list:
                r += job.result
        else:
            return 'ERROR: merge_job_results() was called when all jobs werent complete', 415
    return r

# new to 4.2.0
def job_status_reactapp_grouped(job_id):
    '''
    Retrieves a dictionary of job_id from Redis (not RQ) and checks
    status of all jobs
    Returns the complete result only if all jobs are finished
    '''
    # start a redis connection
    redis_url = current_app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    # Retrieves jobs_dict
    jobs_dict = redis_connection.get(job_id)
    # redis-py returns a string by default
    # we cast this using ast.literal_eval()
    # the alt. is to set a response callback via redis_connection.set_response_callback()
    jobs_dict = literal_eval(jobs_dict)
    print jobs_dict
    # print type(jobs_dict)
    for key in jobs_dict:
        key = str(key)
        # print key
        job = fetch_job(key)
        # print job
        if job.is_failed:
            return jsonify(job.exc_info)
        elif not job.is_finished:
            return jsonify("pending")
    # if you've gotten to this point, then all jobs are finished
    return jsonify(merge_job_results(jobs_dict))

@bp_ra.route('/api/v0/results/<job_id>')
def job_status_reactapp(job_id):
    '''
    This provides an endpoint for the reactapp to poll results. We leave job_status() intact to maintain backwards compatibility with the AngularJS app.
    '''
    # new to 4.2.0
    # check if the job_id is of the new format and should be handled diff
    if job_id.startswith('blob'):
        return job_status_reactapp_grouped(job_id)
    else:
        # old code
        job = fetch_job(job_id)
        if job.is_finished:
            r = job.result
            # subtyping results come in the form of a list and must
            # be conv to json otherwise, you get a 500 error (isa)
            if type(r) is list:
                return jsonify(r)
            # fishers results come in the form of a df.to_json object
            # and should be returned directly
            else:
                return job.result
        elif job.is_failed:
            return jsonify(job.exc_info)
        else:
            return jsonify("pending")

@bp_ra.route('/api/v0/newgroupcomparison', methods=['POST'])
def handle_group_comparison_submission():
    query = request.json['groups']
    target = request.json['target']
    jobid = blob_gc_enqueue(query, target)
    return jobid

@bp_ra.route('/api/v0/get_attribute_values/type/<path:attributetype>')
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

@bp_ra.route('/api/v0/get_all_types')
def combine_types():
    '''
    Returns all URIs that is either a attribute type or and object type.
    '''
    set_attribute_types = set(get_all_attribute_types())
    set_object_types = get_types() # get types returns a set by default
    return jsonify(list(set_attribute_types.union(set_object_types)))

@bp_ra.route('/api/v0/get_all_attribute_types')
def call_get_all_atribute_types():
    '''
    Front-End API:
    Get all possible attribute types.
    '''
    return jsonify(get_all_attribute_types())
