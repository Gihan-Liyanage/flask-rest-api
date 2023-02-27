from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed

from .users.views import user_namespace
from .authentication.views import authentication_namespace
from .classes.views import class_namespace
from .config.config import config_dict
from .utils import db
from .models.users import User

def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt=JWTManager(app)
    migrate=Migrate(app, db)

    api = Api(app)

    @api.errorhandler(NotFound)
    def not_found(error):
        return {
            "error": "Not Found",
            "message": error.message | error
        }, 404
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {
            "error": "Method Not Allowed",
            "message": error.message | error
        }, 405

    api.add_namespace(user_namespace, path='/user')
    api.add_namespace(authentication_namespace, path='/auth')
    api.add_namespace(class_namespace, path='/class')

    return app