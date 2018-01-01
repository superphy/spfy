'''
This is the app factory used to geenrate an instance of the Flask app.
'''

from flask import Flask, jsonify

from flask_recaptcha import ReCaptcha
from flask_cors import CORS, cross_origin
from raven.contrib.flask import Sentry
# from flask_mail import Mail
# from flask_wtf.csrf import CSRFProtect

import config

from routes.views import bp as spfy
from routes.ra_views import bp_ra_views
from routes.ra_posts import bp_ra_posts
from routes.ra_statuses import bp_ra_statuses
from routes.ra_module_database import bp_ra_db
from routes.ra_module_metadata import bp_ra_meta
from routes.ra_pan import bp_ra_pan
from routes.alive import bp_alive
# from routes.ra_accounts import main_blueprint
from routes.ra_restricted import bp_ra_restricted

# Instantiate Flask extensions
db = SQLAlchemy()
# csrf_protect = CSRFProtect()
# mail = Mail()
migrate = Migrate()

# Auth0
# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def create_app():
    app = Flask(__name__)

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    ## Flask Configs
    app.config.from_object(config)
    app.config.from_envvar('LOCAL_SETTINGS', silent=True)

    # disable strict slashes
    # this makes routes defined without trailing / applicable to requests with or w/o the slashes
    # ex. @bp.route('/users') can be accessed via /users or /users/
    app.url_map.strict_slashes = False

    ## Extensions

    # ReCaptcha
    recaptcha = ReCaptcha()
    recaptcha.init_app(app)

    # CORS
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Sentry
    if hasattr(config, 'SENTRY_DSN'):
        sentry = Sentry(dsn=config.SENTRY_DSN)
        sentry.init_app(app)

    # # Setup Flask-Mail
    # mail.init_app(app)
    #
    # # Setup WTForms CSRFProtect
    # csrf_protect.init_app(app)

    ## Routes
    app.register_blueprint(spfy)
    # register the new blueprints used by reactapp
    app.register_blueprint(bp_ra_views)
    app.register_blueprint(bp_ra_posts)
    app.register_blueprint(bp_ra_statuses)
    app.register_blueprint(bp_ra_db)
    app.register_blueprint(bp_ra_meta)
    app.register_blueprint(bp_ra_pan)
    app.register_blueprint(bp_alive)
    # app.register_blueprint(main_blueprint)
    app.register_blueprint(bp_ra_restricted)

    return app
