from flask import request, jsonify
from flask_jwt_extended import create_access_token

from app.api import APIView
from app.blueprints.user.models import User
from app.blueprints.user.schemas import auth_schema


class AuthView(APIView):
    def post(self):
        json_data = request.get_json()

        if not json_data:
            response = jsonify({
                'error': 'Invalid input.'
            })
            return response, 400

        data, errors = auth_schema.load(json_data)

        if errors:
            response = jsonify({
                'error': errors
            })

            return response, 422

        user = User.find_by_identity(data['identity'])

        if user and user.authenticated(password=data['password']):
            # identity is used to lookup a user on protected endpoints
            access_token = create_access_token(identity=user.username)

            response = jsonify({
                'data': {
                    'access_token': access_token
                }
            })

            return response, 200

        response = jsonify({
            'error': 'Invalid credentials.'
        })
        return response, 401
