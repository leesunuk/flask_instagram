from turtle import pos
from marshmallow import ValidationError
from flask_restful import Resource, request
from api.models.post import PostModel
from api.schemas.post import PostSchema

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
    def put(cls, id):
        post_json = request.get_json()
        post = PostModel.find_by_id(id)
        
        if post:
            post.title = post_json["title"]
            post.content = post_json["content"]
        else:
            try:
                post = post_schema.load(post_json)
            except ValidationError as err:
                return err.messages, 400
        
        post.save_to_db()
        
        return post_schema.dump(post), 200
    
    @classmethod
    def delete(cls, id):
        post = PostModel.find_by_id(id)
        if post:
            post.delete_from_db()
            return {"message" : "게시물이 삭제되었습니다."}, 200
        return {"Error" : "게시물을 찾을 수 없습니다."},404

class PostList(Resource):
    @classmethod
    def get(cls):
        return {"posts" : post_list_schema.dump(PostModel.find_all())}, 200
    
    @classmethod
    def post(cls):
        post_json = request.get_json()
        try:
            new_post = post_schema.load(post_json)
        except ValidationError as err:
            return err.messages, 400
        
        try:
            new_post.save_to_db()
        except:
            return {"Error" : "저장에 실패했습니다."}, 500
        
        return post_schema.dump(new_post), 201