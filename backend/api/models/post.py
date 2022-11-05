from ..db import db
from sqlalchemy.sql import func


class PostModel(db.Model):

    __tablename__ = "Post"

    id = db.Column(db.Integer, primary_key=True) # 기본 키
    title = db.Column(db.String(150)) # 제목, 150자 제한
    content = db.Column(db.String(500)) #내용, 500자 제한
    created_at = db.Column(db.DateTime(timezone=True), default=func.now()) #생성일, 현재로 저장
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now()) #업데이트 날짜, 수정될 때마다 그 시간으로 수정됨
    author_id = db.Column(db.Integer, db.ForeignKey("User.id", ondelete="CASCADE"), nullable=False) # 글쓴이, 외래키, 외래키가 삭제되면 글이 같이 삭제됨, 필수
    author = db.relationship("UserModel", backref="post_author") 
    comment_set = db.relationship("CommentModel", backref="post", passive_deletes=True) # 댓글

    @classmethod
    def find_by_id(cls, id): # id로 검색
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    

    def save_to_db(self): # 저장
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self): #삭제
        db.session.delete(self)
        db.session.commit()
        
    def update_to_db(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    def __repr__(self):
        return f"<Post Object : {self.title}>"