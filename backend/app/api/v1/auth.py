from flask import request as flask_request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from ...models import User
from ...extensions import db

api = Namespace('auth', description='Authentication')

login_model = api.model('Login', {
    'email': fields.String(required=True),
})

tokens_model = api.model('Tokens', {
    'access_token': fields.String,
    'refresh_token': fields.String,
})


@api.route('/login')
class LoginResource(Resource):
    @api.expect(login_model, validate=True)
    @api.marshal_with(tokens_model)
    def post(self):
        payload = flask_request.get_json()
        email = payload['email']
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, full_name=email.split('@')[0].title(), role='requester')
            db.session.add(user)
            db.session.commit()
        identity = {'id': user.id, 'role': user.role}
        return {
            'access_token': create_access_token(identity=identity),
            'refresh_token': create_refresh_token(identity=identity),
        }


@api.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    @api.marshal_with(tokens_model)
    def post(self):
        identity = get_jwt_identity()
        return {
            'access_token': create_access_token(identity=identity),
            'refresh_token': create_refresh_token(identity=identity),
        }


@api.route('/me')
class MeResource(Resource):
    @jwt_required()
    def get(self):
        return get_jwt_identity()