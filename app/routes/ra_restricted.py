from flask import Blueprint, request, jsonify
from middleware.auth import get_token_auth_header, requires_simple_auth
from middleware.mongo import mongo_update, mongo_find

bp_ra_restricted = Blueprint('reactapp_restricted', __name__)

@bp_ra_restricted.route("/api/v0/secured/simple/ping")
@requires_simple_auth
def secured_simple_ping():
    """A valid access token and an appropriate scope are required to access this route.
    Used in tests of token authentication.
    """
    return "All good. You only get this message if you're authenticated"

@bp_ra_restricted.route("/api/v0/secured/accounts/update", methods=['POST'])
@requires_simple_auth
def update():
    uid = get_token_auth_header()
    print('update() request')
    json = request.json
    print(json)
    # Get the store currently in the database.
    previous_store = mongo_find(uid)
    assert type(previous_store) is list
    hashes = set()
    # Create a set of the hashes.
    for item in previous_store:
        # Check if the item (eg. the job) has a hash.
        if 'hash' in item:
            hashes.add(item['hash'])
    # Check the update.
    for item in json:
        if 'hash' in item and item['hash'] not in hashes:
            previous_store.append(item)
    # The previous_store should now be merged with the update.
    print('update()', json)
    mongo_update(uid, previous_store)
    return jsonify('success!')

@bp_ra_restricted.route("/api/v0/secured/accounts/find")
@requires_simple_auth
def find():
    uid = get_token_auth_header()
    store = mongo_find(uid)
    return jsonify(store)
