from api.models.user import UserModel, RefreshTokenModel
from flask_restful import Resource, request
from api.schemas.user import UserRegisterSchema
from werkzeug.security import generate_password_hash
from flask_jwt_extended import(
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from flask.views import MethodView
from werkzeug.security import check_password_hash
register_schema = UserRegisterSchema()


class UserRegister(Resource):
    
    def post(self):
        data = request.get_json()
        validate_result = register_schema.validate(data)
        if validate_result:
            return validate_result, 400
        else:
            if UserModel.find_by_username(data["username"]):
                return {"bad request": "중복된 사용자 이름입니다."}, 400
            elif UserModel.find_by_email(data["email"]):
                return {"message": "중복된 이메일입니다."}, 400
            else:
                password = generate_password_hash(data["password"])
                user = register_schema.load({
                    "username" : data["username"],
                    "email" : data["email"],
                    "password" : password,
                    "password_confirm" : password,
                })
            user.save_to_db()
            return {"success": f"{user.username} 님, 가입을 환영합니다!"}, 201
        
class UserLogin(MethodView):
    def post(self):
        data = request.get_json()
        user = UserModel.find_by_email(data["email"])
        
        if user and check_password_hash(user.password, data["password"]):
            access_token = create_access_token(identity=user.username, fresh=True)
            refresh_token = create_refresh_token(identity=user.username)
            
            if user.token:
                token = user.token[0]
                token.refresh_token_value = refresh_token
                token.save_to_db()
            else:
                new_token = RefreshTokenModel(user_id=user.id, refresh_token_value=refresh_token)
                new_token.save_to_db()
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
    
        return {"Unauthorized": "이메일과 비밀번호를 확인하세요."}, 401
    
class RefreshToken(MethodView):

    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        token = dict(request.headers)["Authorization"][7:]
        user = RefreshTokenModel.get_user_by_token(token)
        if not user:
            return {"Unauthorized": "Refresh Token은 2회 이상 사용될 수 없습니다."}, 401
        # access token, refresh token 발급
        access_token = create_access_token(fresh=True, identity=identity)
        refresh_token = create_refresh_token(identity=user.username)
        if user:
            token = user.token[0]
            token.refresh_token_value = refresh_token
            token.save_to_db()
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        
            
    @classmethod
    def get_user_by_token(cls, token):
        
        try:
            user_id = cls.query.filter_by(refresh_token_value=token).first().user_id
        except AttributeError:
            return None
        user = UserModel.find_by_id(id=user_id)
        return user