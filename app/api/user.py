from flask import request, jsonify
from marshmallow import ValidationError

from app.api import APIView
from app.blueprints.user.models import User
from app.blueprints.user.schemas import registration_schema


class UsersView(APIView):
    def post(self):
        json_data = request.get_json()

        if not json_data:
            response = {'error': 'Invalid input.'}
            return jsonify(response), 400

        try:
            data = registration_schema.load(json_data)
        except ValidationError as err:
            response = jsonify({
                'error': err.messages
            })
            return response, 422

        user = User()
        user.email = data.get('email')
        user.username = data.get('username')
        user.password = User.encrypt_password(data.get('password'))
        user.save()

        return jsonify({}), 201
