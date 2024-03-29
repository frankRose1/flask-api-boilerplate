"""
 Init an instance of each extension used in the Flask app here
"""
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

jwt = JWTManager()
db = SQLAlchemy()
ma = Marshmallow()
