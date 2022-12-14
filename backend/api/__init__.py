from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv
from flask_cors import CORS

from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_uploads import configure_uploads, patch_request_class
from marshmallow import ValidationError

from api.utils.image_upload import IMAGE_SET

from datetime import timedelta

from .db import db
from .ma import ma
from .models import user, post, comment

from .resources.post import PostList, Post
from .resources.user import UserRegister, UserLogin, RefreshToken
from .resources.image import *



def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins":"*"}})
    load_dotenv(".env", verbose=True)
    app.config.from_object("config.dev")
    app.config.from_envvar("APPLICATION_SETTINGS")
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    app.config["JSON_AS_ASCII"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    
    configure_uploads(app, IMAGE_SET)
    
    api = Api(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
    @app.before_first_request
    def create_tables():
        db.create_all
        
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400
    
    api.add_resource(PostList, "/posts/")
    api.add_resource(Post, "/posts/<int:id>")
    api.add_resource(UserRegister, "/register/")
    api.add_resource(UserLogin, "/login/")
    api.add_resource(RefreshToken, "/refresh")
    api.add_resource(PostImageUpload, "/upload/post/image/")
    api.add_resource(ProfileImageUpload, "/upload/profile/image/")
    api.add_resource(Image, "/statics/<path:path>")
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """
        토큰이 만료되었을 때의 에러 메시지를 지정합니다.
        """
        return (
            jsonify({"Error": "토큰이 만료되었습니다."}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """
        토큰이 잘못된 값일 때의 에러 메시지를 지정합니다.
        """
        return (
            jsonify({"Error": "잘못된 토큰입니다."}),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """ """
        return (
            jsonify(
                {
                    "Error": "토큰 정보가 필요합니다.",
                }
            ),
            401,
        )
    return app

