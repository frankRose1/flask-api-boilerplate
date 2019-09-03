from flask import Flask, jsonify

from app.api.auth import AuthView
from app.api.user import UsersView
from app.extensions import (
    jwt,
    db,
    ma
)

def create_app(settings_override=None):
    """
    Create a Flask app using the app factory pattern

    :param settings_override: Overide app settings
    :type settings_override: dict
    :return: Flask app instance
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')

    # use instance/settings.py(if it exists)
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    # Register API views
    AuthView.register(app)
    UsersView.register(app)

    jwt_callbacks()

    # Add extensions
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
