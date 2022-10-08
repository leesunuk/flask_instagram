from ..db import db


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True), # 나를 팔로우하는 사람들의 id
    db.Column('followed_id', db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True) # 내가 팔로우한 사람들의 id
)

class UserModel(db.Model):
    __tablename__ = "User"
    
    id = db.Column(db.Integer, primary_key=True) # 기본 키
    username = db.Column(db.String(80), nullable=False, unique=True) # 80자 제한, 중복 X, 필수
    password = db.Column(db.String(80), nullable=False) # 80자 제한, 필수
    email = db.Column(db.String(80), nullable=False, unique=True) # 중복 X, 필수
    created_at = db.Column(db.DateTime, server_default=db.func.now()) # 가입 날짜

    followed = db.relationship(                             # 본인이 팔로우한 유저들
        'UserModel',                                        # User 모델 스스로를 참조
        secondary=followers,                                # 연관 테이블 이름을 지정
        primaryjoin=(followers.c.follower_id==id),          # followers 테이블에서 특정 유저를 팔로우하는 유저들을 찾음
        secondaryjoin=(followers.c.followed_id==id),        # followers 테이블에서 특정 유저가 팔로우한 모든 유저들을 찾음
        backref=db.backref('follower_set', lazy='dynamic'), # 역참조 관계 설정
        lazy='dynamic' 
    )
    
    def follow(self, user): # 팔로우
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user): # 언팔로우

        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user): # 현재 사용자의 특정 사용자 팔로우 여부 반환 (True or False)
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    @classmethod
    def find_by_username(cls, username): # db에서 이름으로 사용자 찾기

        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, id): # db에서 id 로 사용자 찾기   
        return cls.query.filter_by(id=id).first()
    
    def save_to_db(self): # 사용자를 db에 저장

        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self): # 사용자를 db에서 삭제

        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<User Object : {self.username}>'