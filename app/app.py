from flask import Flask


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
    pass
