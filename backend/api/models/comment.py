from ..db import db
from sqlalchemy.sql import func


class CommentModel(db.Model):

    __tablename__ = "Comment"
       
    id = db.Column(db.Integer, primary_key=True) # 기본 키
    content = db.Column(db.Text(), nullable=False) # 내용, 필수
    created_at = db.Column(db.DateTime(timezone=True), default=func.now()) #생성일, 현재로 저장
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now()) #업데이트 일, 업데이트 시점 저장
    author_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False) #댓글 쓴 사람, 외래키, 외래키 삭제시 같이 삭제됨, 필수
    author = db.relationship("UserModel", backref="comment_author")
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id', ondelete='CASCADE'), nullable=False) #댓글의 본문, 외래키, 외래키 삭제시 같이 삭제, 필수
    
    def save_to_db(self): # 저장
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self): #삭제
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def find_by_id(cls, id): #id로 검색   
        return cls.query.filter_by(id=id).first()
        
    def __repr__(self):
        return f'<Comment Object : {self.content}>'