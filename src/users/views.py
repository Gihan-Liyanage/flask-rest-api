from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User, UserTypes
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from http import HTTPStatus
from password_generator import PasswordGenerator
from werkzeug.exceptions import Unauthorized, Conflict

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
        loggedin_username=get_jwt_identity()
        data = request.get_json()
        password = pwo.generate()
        new_username= data.get('username')

        loggedin_user = User.query.filter_by(username=loggedin_username).first()

        if loggedin_user.usertype not in [UserTypes.ADMIN, UserTypes.INSTRUCTOR]:
            raise Unauthorized("Unauthorized Request")
        
        new_user = User.query.filter_by(username=new_username).first()

        if new_user is not None:
            raise Conflict(f"User with username {new_username} already exists")

        new_student = User(
            username=new_username,
            passwordhash=generate_password_hash(password),
            usertype=UserTypes.STUDENT
        )

        new_student.save()

        return {"password": password}, HTTPStatus.CREATED
    

@user_namespace.route('/instructor')
class Instructor(Resource):

    @user_namespace.expect(user_signup_request)
    @user_namespace.marshal_with(user_signup_response)
    @jwt_required()
    def post(self):
        """Signup new instructors
        """
        loggedin_username=get_jwt_identity()
        data = request.get_json()
        password = pwo.generate()
        new_username= data.get('username')

        loggedin_user = User.query.filter_by(username=loggedin_username).first()

        if loggedin_user.usertype is not UserTypes.ADMIN:
            raise Unauthorized("Unauthorized Request")
        
        new_user = User.query.filter_by(username=new_username).first()

        if new_user is not None:
            raise Conflict(f"User with username {new_username} already exists")

        new_user = User(
            username=new_username,
            passwordhash=generate_password_hash(password)
        )

        new_user.save()

        return {"password": password}, HTTPStatus.CREATED