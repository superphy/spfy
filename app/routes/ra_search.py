import os
import flask
import werkzeug
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_recaptcha import ReCaptcha
from werkzeug.utils import secure_filename
from modules.search import blob_search_enqueue

bp_ra_search = Blueprint('reactapp_search', __name__)

@bp_ra_search.route('/api/v0/search', methods=['POST'])
def search_file():
    recaptcha = ReCaptcha(app=current_app)
    if not recaptcha.verify():
        return "Captcha Failed Verification", 403

    # Initial.
    form = request.form
    if 'st' not in form.keys():
        return "Invalid Name", 400
    s = ''

    # Processing form data.
    for key, value in form.items():
        if key == 'st':
            s = value

    # Create a search job.
    jobid = blob_search_enqueue(s)
    return jobid
