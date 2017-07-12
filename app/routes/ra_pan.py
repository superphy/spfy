from flask import Blueprint, request, jsonify

bp_ra_posts = Blueprint('reactapp_posts', __name__)


# if methods is not defined, default only allows GET
@bp_ra_posts.route('/api/v0/panseq', methods=['POST'])
def pan_route():
  form = request.form
  return jsonify('Got your form')
