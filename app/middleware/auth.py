import hashlib
import random

from functools import wraps
from datetime import datetime
from flask import Flask, request, jsonify, _app_ctx_stack
from middleware.mongo import mongo_find, mongo_update

# Auth0
# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Format error response and append status code
def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def validate_simple(token):
    """Checks that the given token exists
    in MongoDB.
    """
    status = mongo_find(token, 'status')
    return status == "active"

def requires_simple_auth(f):
    """A simple authentication check.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        try:
            assert validate_simple(token) == True
        except Exception:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Token doesn't exist"
                                " token."}, 400)
        return f(*args, **kwargs)
    return decorated

def _generate_token():
    """
    Generates a bearer token for use by the front-end.
    Not actually secure, but suffices for our uses.
    """
    now = datetime.now()
    now = now.strftime("%Y-%m-%d-%H-%M-%S-%f")
    salt = random.randint(100000,999999)
    seed = "{0}{1}".format(now,salt)
    token = hashlib.sha1(seed).hexdigest()
    return token

def _store(token):
    """
    Stores the bearer token to MongoDB.
    """
    # We should add a check for collision, but it's unlikely we'll see any.
    # Add the account to mongo.
    mongo_update(token, 'active', 'status')
    # Create an empty jobs dictionary for the account.
    mongo_update(token)

def bearer():
    token = _generate_token()
    _store(token)
    return token