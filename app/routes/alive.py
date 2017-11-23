from flask import Blueprint, jsonify

bp_alive = Blueprint('alive', __name__)

@bp_alive('/api/v0/alive')
def alive():
    '''
    Used for tests to check if the webserver is working internally.
    This route is queryed by PyTest.
    '''
    # Lowercase true to distinguish from Python's True.
    return jsonify('true')
