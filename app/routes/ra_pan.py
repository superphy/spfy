import os
import tarfile
import zipfile
import redis
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_recaptcha import ReCaptcha
from werkzeug.utils import secure_filename
from routes.file_utils import fix_uri, handle_tar, handle_zip
from routes.ra_api import subtyping_dependencies
from modules.gc import blob_gc_enqueue
from modules.spfy import spfy
from routes.ra_posts import handle_groupresults, handle_singleton

bp_ra_posts = Blueprint('reactapp_posts', __name__)


# if methods is not defined, default only allows GET
@bp_ra_posts.route('/api/v0/panseq', methods=['POST'])
def pan_route():
  form = request.form
  return jsonify('Got your form')

@bp_ra_posts.route('/api/v0/upload', methods=['POST'])
def upload():
    recaptcha = ReCaptcha(app=current_app)
    if recaptcha.verify():
        form = request.form
        options = {}
        # defaults
        options['pi']=90
        options['pan'] = True
        options['amr']=True
        options['vf']=True
        options['serotype']=True


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
                if key == 'options.bulk':
                    options['bulk'] = value
            else:
                if key =='options.pi':
                    options['pi']=int(value)

        # get a list of files submitted
        uploaded_files = request.files.getlist("file")
        print uploaded_files

        print 'upload(): about to enqueue files'
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
                #print 'Uploaded File Saved at', str(filename)

                if tarfile.is_tarfile(filename):
                    # set filename to dir for spfy call
                    filename = handle_tar(filename, now)
                elif zipfile.is_zipfile(filename):
                    filename = handle_zip(filename, now)
                if not pan:
                    # for enqueing task
                    jobs_enqueued = spfy(
                        {'i': filename, 'pi':options['pi'], 'options':options})
                    jobs_dict.update(jobs_enqueued)
        # new in 4.2.0
        if pan:
            jobs_enqueued = spfy9({'i': uploaded_files, 'pi':options['pi'], 'options':options})
            jobs_dict.update(jobs_enqueued)
                    
        print 'upload(): all files enqueued, returning...'
        if groupresults:
            return jsonify(handle_groupresults(jobs_dict))
        else:
            return jsonify(handle_singleton(jobs_dict))
    else:
        return "Captcha Failed Verification", 500
