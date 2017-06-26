from flask import Blueprint
from modules.database import blob_db_enqueue

bp_ra_db = Blueprint('reactapp_module_database', __name__)

# this is for the Group Comparisons (Fishers) module
@bp_ra_db.route('/api/v0/newdatabasestatus', methods=['POST'])
def handle_group_comparison_submission():
    jobid = blob_db_enqueue()
    return jobid
