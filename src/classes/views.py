import json
from flask_restx import Namespace, Resource, fields
from flask import request
from sqlalchemy import and_
from werkzeug.security import generate_password_hash
from password_generator import PasswordGenerator
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import Unauthorized, Conflict

from ..models.classes import Class, Modules
from ..models.users import User, UserTypes
from ..utils import db

pwo = PasswordGenerator()

class_namespace=Namespace('classes', description="Classes related endpoints")

create_class_model=class_namespace.model(
    "Create_Class", {
        'name': fields.String(required=True, description='A name for the class'),
        'students': fields.List(cls_or_instance=fields.String(), required=True, description='List of students'),
        'module':  fields.String(required=True, description='ML Module', enum=['IMAGE_PROCESSING', 'VOICE_REC', 'FACE_DETECT']),
    }
)

modules_model=class_namespace.model(
    "Module", {
     'classname': fields.String(enum=['IMAGE_PROCESSING', 'VOICE_REC', 'FACE_DETECT'], required=True, description='List of modules'),
    }
)

@class_namespace.route('')
class Classes(Resource):
    @class_namespace.expect(create_class_model)
    @jwt_required()
    @class_namespace.doc(
        description="Create new class. authorized only for instructors",
        responses={
            201: "Common password for created class"
        }
    )
    def post(self):
        """Create new classes
        """
        username=get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        request_data=request.get_json()
        class_name=request_data.get('name')
        
        if not user:
            raise Unauthorized("Unauthorized Request")

        if user.usertype is not UserTypes.INSTRUCTOR:
            raise Unauthorized("User without permissions!")

        existing_class = Class.query.filter_by(name=class_name).first()

        if existing_class is not None:
            raise Conflict(f"Class with name {class_name} already exists")

        password = pwo.generate()

        student_list = list(request_data.get('students'))

        students = User.query.filter(User.username.in_(student_list)).all()

        new_class = Class(
            name=class_name,
            module=request_data.get('module'),
            passwordhash=generate_password_hash(password)
        )

        for student in students:
             new_class.attending.append(student)

        new_class.save()

        db.session.commit()

        return {"password": password}, HTTPStatus.CREATED


@class_namespace.route('/module/view')
class ViewModule(Resource):

    @class_namespace.expect(modules_model)
    @class_namespace.doc(
        description="View available modules for the user",
        responses={
            200: "Available modules"
        }
    )
    @jwt_required()
    def post(self):
        """View modules
        """
        username=get_jwt_identity()
        class_name=request.get_json().get('classname')

        user = User.query.filter_by(username=username).first()

        if not user:
            raise Unauthorized("Unauthorized Request")

        if user.usertype in [UserTypes.INSTRUCTOR, UserTypes.ADMIN]:
            return {"modules": Modules._member_names_}, HTTPStatus.OK

        else:
            classes = Class.query.filter(and_(Class.attending.any(id=user.id), Class.name==class_name)).all()
            return {"module": classes[0].module}, HTTPStatus.OK

@class_namespace.route('/module/execute')
class ExecuteModule(Resource):

    @class_namespace.expect(modules_model)
    @class_namespace.doc(
        description="Execute modules when the class is given",
        responses={
            200: "Hello [Available Modules]"
        }
    )
    @jwt_required()
    def post(self):
        """Return all the classes
        """
        username=get_jwt_identity()
        class_name=request.get_json().get('classname')

        user = User.query.filter_by(username=username).first()

        if not user:
            raise Unauthorized("Unauthorized Request")

        if user.usertype in [UserTypes.INSTRUCTOR, UserTypes.ADMIN]:
            return {"message": f"Hello {Modules._member_names_}"}, HTTPStatus.OK

        else:
            class_data = Class.query.filter(and_(Class.attending.any(id=user.id), Class.name==class_name)).all()
            return {"message": f"Hello {class_data[0].module}"}, HTTPStatus.OK
