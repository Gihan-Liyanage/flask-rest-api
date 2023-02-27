from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import check_password_hash
from password_generator import PasswordGenerator
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from werkzeug.exceptions import Forbidden

pwo = PasswordGenerator()

authentication_namespace = Namespace(
    'auth', description="Authentication Endpoints"
)

login_request = authentication_namespace.model(
    "Login", {
        'username': fields.String(required=True, description="A username"),
        'password': fields.String(required=True, description="A Password")
    }
)

login_response = authentication_namespace.model(
    "Tokens", {
        'access_token': fields.String(required=True, description="A access token"),
        'refresh_token': fields.String(required=True, description="A refresh token")
    }
)

@authentication_namespace.route('/login')
class Login(Resource):
    @authentication_namespace.expect(login_request)
    @authentication_namespace.doc(
        description="Login users using a username and a password",
        responses={
            200: "Request and access tokens for the user"
        }
    )
    def post(self):
        """Login user
        """
        request_data = request.get_json()
        username = request_data.get('username')
        password = request_data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.passwordhash,password):
            access_token = create_access_token(identity=username)
            refresh_token=create_refresh_token(identity=username)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, HTTPStatus.OK
        
        raise Forbidden("Invalid Username or Password")


@authentication_namespace.route('/refresh')
class Refresh(Resource):

    @jwt_required(refresh=True)
    @authentication_namespace.doc(
        description="Generate access token given the refresh token",
        responses={
            200: "New access token"
        }
    )
    def post(self):
        """Generate access token given the refresh token
        """
        username=get_jwt_identity()

        access_token=create_access_token(identity=username)

        return {'access_token':access_token},HTTPStatus.OK
