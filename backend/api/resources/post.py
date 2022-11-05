from turtle import pos
from marshmallow import ValidationError
from flask_restful import Resource, request
from api.models.post import PostModel
from api.models.user import UserModel
from api.schemas.post import PostSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

post_schema = PostSchema()
post_list_schema = PostSchema(many=True)

class Post(Resource):
    @classmethod
    def get(cls, id):
        post = PostModel.find_by_id(id)
        if post:
            return post_schema.dump(post), 200
        return {"Error" : "게시물을 찾을 수 없습니다."}, 404
    
    @classmethod
    @jwt_required()
    def put(cls, id):
        post_json = request.get_json()
        validate_result = post_schema.validate(post_json)
        
        if validate_result:
            return validate_result, 400
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        post = PostModel.find_by_id(id)
        
        if not post:
            return {"Error": "게시물을 찾을 수 없습니다."}, 404

        
        if post.author_id == author_id:
            post.update_to_db(post_json)
        else:
            return {"Error": "게시물은 작성자만 수정할 수 있습니다."}, 403

        return post_schema.dump(post), 200
    
    @classmethod
    @jwt_required
    def delete(cls, id):
        post = PostModel.find_by_id(id)
        if post:
            post.delete_from_db()
            return {"message" : "게시물이 삭제되었습니다."}, 200
        return {"Error" : "게시물을 찾을 수 없습니다."},404

class PostList(Resource):
    @classmethod
    def get(cls):
        page = request.args.get("page", type=int, default=1)
        orderd_posts = PostModel.query.order_by(PostModel.id.desc())
        pagination = orderd_posts.paginate(page, per_page=10, error_out=False)
        result = post_list_schema.dump(pagination.items)
        return result
        # return {"posts" : post_list_schema.dump(PostModel.find_all())}, 200
    
    @classmethod
    @jwt_required()
    def post(cls):
        post_json = request.get_json()
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        
        try:
            new_post = post_schema.load(post_json)
            new_post.author_id = author_id
        except ValidationError as err:
            return err.messages, 400
        
        try:
            new_post.save_to_db()
        except:
            return {"Error" : "저장에 실패했습니다."}, 500
        
        return post_schema.dump(new_post), 201