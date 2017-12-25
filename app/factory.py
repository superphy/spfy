'''
This is the app factory used to geenrate an instance of the Flask app.
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin
import config
from routes.views import bp as spfy
from routes.ra_views import bp_ra_views
from routes.ra_posts import bp_ra_posts
from routes.ra_statuses import bp_ra_statuses
from routes.ra_module_database import bp_ra_db
from routes.ra_module_metadata import bp_ra_meta
from flask_recaptcha import ReCaptcha
from flask_cors import CORS, cross_origin
from raven.contrib.flask import Sentry
from routes.ra_pan import bp_ra_pan
from routes.alive import bp_alive

def create_app():
    app = Flask(__name__)

    ## Flask Configs
    app.config.from_object(config)
    app.config.from_envvar('LOCAL_SETTINGS', silent=True)

    # disable strict slashes
    # this makes routes defined without trailing / applicable to requests with or w/o the slashes
    # ex. @bp.route('/users') can be accessed via /users or /users/
    app.url_map.strict_slashes = False

    ## Extensions
    recaptcha = ReCaptcha()
    recaptcha.init_app(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    # sentry
    if hasattr(config, 'SENTRY_DSN'):
        sentry = Sentry(dsn=config.SENTRY_DSN)
        sentry.init_app(app)

    # Initialize Flask-SQLAlchemy
    db = SQLAlchemy(app)
    # Define the User data-model.
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

        # User authentication information
        username = db.Column(db.String(100), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')
        email_confirmed_at = db.Column(db.DateTime())

        # User information
        first_name = db.Column(db.String(100), nullable=False, server_default='')
        last_name = db.Column(db.String(100), nullable=False, server_default='')
    # Create all database tables
    db.create_all()
    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

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

    return app
