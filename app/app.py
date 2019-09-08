from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, jsonify

from app.blueprints.user.models import User
from app.api.auth import AuthView
from app.api.user import UsersView
from app.api.health_check import HealthyView
from app.extensions import (
    jwt,
    db,
    ma
)

# This is where you put the path to your background tasks as a string
# eg 'app.blueprints.user.tasks'
CELERY_TASK_LIST = []


def create_celery_app(app=None):
    """
    Create a new Celery object and sync the Celery config to the Flask app's
    config. Wrap all tasks in the context of the Flask app.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            # if the db is needed inside a task app context must be set
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(settings_override=None):
    """
    Create a Flask app using the app factory pattern

    :param settings_override: Overide app settings
    :type settings_override: dict
    :return: Flask app instance
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')

    if settings_override:
        app.config.update(settings_override)

    middleware(app)

    # Register API views
    HealthyView.register(app)
    AuthView.register(app)
    UsersView.register(app)

    jwt_callbacks()
    extensions(app)

    return app


def extensions(app):
    """
    Add 0 or more extensions to the flask application.
    Mutates the app passed in.

    :param app: Flask application instance
    :return: None
    """
    jwt.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    return None


def jwt_callbacks():
    """
    Set up custom behavior for JWT authentication.

    :return: None
    """
    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):
        """
        This is called when a user accesses a protected endpoint and it will
        populate "flask_jwt.current_user" with the loaded user.

        :param identity: Is which ever unique identity you chose when creating
        the access token.
        :return: User model instance
        """
        return User.query.filter(User.username == identity).first()

    @jwt.user_claims_loader
    def add_claims_to_access_token_callback(identity):
        """
        This is called when ever an access token is created. It will add any
        additional info regarding the user to the access token. For example
        you may use it to determine if a user has admin permissions or not

        :param identity: Is which ever unique identity you chose when creating
        the access token.
        :return: dict
        """
        user =  User.query.filter(User.username == identity).first()
        return {
            'role': user.role
        }

    @jwt.unauthorized_loader
    def jwt_unauthorized_callback(error):
        response = {
            'error': {
                'message': 'Auth token was not provided.',
                'detail': error
            }
        }

        return jsonify(response), 401

    @jwt.expired_token_loader
    def jwt_expired_token_callback(error):
        response = {
            'error': {
                'message': 'Auth token has expired'
            }
        }

        return jsonify(response), 401

    return None


def middleware(app):
    """
    Register 0 or more middleware (mutates the app passed in)

    :param app: Flask application instance
    :return: None
    """
    # This is necessaary if you plan on using request.remote_addr and you
    # happen to have a proxy in front of your server.
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return None