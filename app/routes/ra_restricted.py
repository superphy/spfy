from flask import Blueprint, request, jsonify
from middleware.auth import requires_auth, requires_scope, get_token_auth_header, requires_simple_auth
from middleware.mongo import mongo_update, mongo_find

bp_ra_restricted = Blueprint('reactapp_restricted', __name__)

@bp_ra_restricted.route('/api/v0/ping')
def ping():
    return "All good. You don't need to be authenticated to call this"

@bp_ra_restricted.route('/api/v0/secured/ping')
@requires_auth
def securedPing():
    return "All good. You only get this message if you're authenticated"

@bp_ra_restricted.route("/api/v0/secured/private/ping")
@requires_auth
def secured_private_ping():
    """A valid access token and an appropriate scope are required to access this route
    """
    if requires_scope("example:scope"):
        return "All good. You're authenticated and the access token has the appropriate scope"
    return "You don't have access to this resource"

@bp_ra_restricted.route("/api/v0/secured/simple/ping")
@requires_simple_auth
def secured_simple_ping():
    """A valid access token and an appropriate scope are required to access this route
    """
    return "All good. You only get this message if you're authenticated"

@bp_ra_restricted.route("/api/v0/secured/accounts/update", methods=['POST'])
@requires_simple_auth
def update():
    uid = get_sub_claim()
    print('update() request:', request)
    json = request.json
    print('update()', json)
    mongo_update(uid,json)
    return jsonify('true')

@bp_ra_restricted.route("/api/v0/secured/accounts/find")
@requires_simple_auth
def find():
    uid = get_token_auth_header()
    store = mongo_find(uid)
    return jsonify(store)
