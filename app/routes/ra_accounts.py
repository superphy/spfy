from flask import Blueprint
from middleware.token import token

bp_ra_accounts = Blueprint('reactapp_accounts', __name__)

@bp_ra_db.route('/api/v0/accounts')
def create_account():
    token = token()
    return token
