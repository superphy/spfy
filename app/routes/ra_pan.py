from flask import Blueprint, request, jsonify

bp_someroutes = Blueprint('someroutes', __name__)

# if methods is not defined, default only allows GET
@bp_someroutes.route('/api/v0/panseq', methods=['POST'])
def pan_route():
  form = request.form
  return jsonify('Got your form')
