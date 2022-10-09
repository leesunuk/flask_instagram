from api.ma import ma, Method
from api.models.post import PostModel

class PostSchema(ma.SQLAlchemyAutoSchema):
    
    author_name = Method("get_author_name")
    
    def get_author_name(self, obj):
        return obj.author.username
    
    
    class Meta:
        model = PostModel
        dump_only = ["author_name",] #읽기 전용
        load_only = ["author_id",] #쓰기 전용
        
        include_fk = True
        load_instance = True
        ordered = True