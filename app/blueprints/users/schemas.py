from marshmallow import fields, validate, ValidaionError

from app.extensions import ma
from app.blueprints.user.models import User

USERNAME_MESSAGE = 'Username must be letters, numbers, and underscores only.'


def ensure_unique_identity(data):
    """
    Ensures that and email or username is not already taken

    :return: data from the request
    """
    user = User.find_by_identity(data)
    if user:
        raise ValidaionError('{0} already exists.'.format(data))

    return data


class RegistrationSchema(ma.Schema):
    email = fields.Email(required=True, validate=ensure_unique_identity)
    username = fields.Str(required=True,
                          validate=[validate.Length(min=3, max=255),
                                    ensure_unique_identity,
                                    validate.Regexp('^\w+$',
                                    error=USERNAME_MESSAGE)])
    password = fields.Str(required=True,
                          validate=validate.Length(min=8, max=128))


class AuthSchema(ma.Schema):
    identity = fields.Str(required=True,
                          validate=validate.Length(min=3, max=255))
    password = fields.Str(required=True,
                          validate=validate.Length(min=8, max=128))


registration_schema = RegistrationSchema()
auth_schema = AuthSchema()