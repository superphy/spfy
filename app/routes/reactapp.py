from flask import Blueprint, request, jsonify
from modules.groupComparisons.frontend_queries import get_all_attribute_types, get_attribute_values, get_types
from routes.utility_functions import fetch_job, fix_uri
from modules.gc import blob_gc_enqueue

bp_ra = Blueprint('reactapp', __name__)

@bp_ra.route('/api/v0/results/<job_id>')
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
