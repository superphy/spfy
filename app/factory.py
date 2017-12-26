'''
This is the app factory used to geenrate an instance of the Flask app.
'''

from flask import Flask

from flask_recaptcha import ReCaptcha
from flask_cors import CORS, cross_origin
from raven.contrib.flask import Sentry
# from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, SQLAlchemyAdapter
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
from routes.ra_accounts import main_blueprint

# Instantiate Flask extensions
db = SQLAlchemy()
# csrf_protect = CSRFProtect()
# mail = Mail()
migrate = Migrate()

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

    # ReCaptcha
    recaptcha = ReCaptcha()
    recaptcha.init_app(app)

    # CORS
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Sentry
    if hasattr(config, 'SENTRY_DSN'):
        sentry = Sentry(dsn=config.SENTRY_DSN)
        sentry.init_app(app)

    # Initialize Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # # Setup Flask-Mail
    # mail.init_app(app)
    #
    # # Setup WTForms CSRFProtect
    # csrf_protect.init_app(app)

    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    # # Setup an error-logger to send emails to app.config.ADMINS
    # init_email_error_handler(app)

    # Setup Flask-User to handle user account related forms
    from .models.user_models import User, MyRegisterForm
    from .views.misc_views import user_profile_page

    db_adapter = SQLAlchemyAdapter(db, User)  # Setup the SQLAlchemy DB Adapter
    user_manager = UserManager(db_adapter, app,  # Init Flask-User and bind to app
                               register_form=MyRegisterForm,  # using a custom register form with UserProfile fields
                               user_profile_view_function=user_profile_page,
    )

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
    app.register_blueprint(main_blueprint)

    return app
