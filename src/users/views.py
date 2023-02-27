from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User, UserTypes
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from http import HTTPStatus
from password_generator import PasswordGenerator
from werkzeug.exceptions import Unauthorized

user_namespace=Namespace('users', description="namespace for users, admin, instructors and students")

pwo = PasswordGenerator()

user_signup_request = user_namespace.model(
    "User_Signup", {
        'username': fields.String(required=True, description='A username')
    }
)

user_signup_response = user_namespace.model(
    "User", {
        'password':  fields.String(required=True, description='User type')
    }
)

@user_namespace.route('/student')
class Student(Resource):
    @user_namespace.expect(user_signup_request)
    @user_namespace.marshal_with(user_signup_response)
    @jwt_required()
    def post(self):
        """Signup new students
        """
        username=get_jwt_identity()

        user = User.query.filter_by(username=username).first()

        if user.usertype not in [UserTypes.ADMIN, UserTypes.INSTRUCTOR]:
                raise Unauthorized("Unauthorized Request")
        
        data = request.get_json()
        password = pwo.generate()

        new_student = User(
            username=data.get('username'),
            passwordhash=generate_password_hash(password),
            usertype=UserTypes.STUDENT
        )

        new_student.save()

        return {"password": password}, HTTPStatus.CREATED
    

@user_namespace.route('/instructor')
class Instructor(Resource):

    def validate_user(self, jwt_token):
        pass

    @user_namespace.expect(user_signup_request)
    @user_namespace.marshal_with(user_signup_response)
    @jwt_required()
    def post(self):
        """Signup new instructors
        """
        username=get_jwt_identity()

        user = User.query.filter_by(username=username).first()

        if user.usertype is not UserTypes.ADMIN:
                raise Unauthorized("Unauthorized Request")
        
        data = request.get_json()
        password = pwo.generate()

        new_user = User(
            username=data.get('username'),
            passwordhash=generate_password_hash(password)
        )

        new_user.save()

        return {"password": password}, HTTPStatus.CREATED