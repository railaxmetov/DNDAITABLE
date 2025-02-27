from sqlalchemy.orm import defer

from backend.config import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def get_id(self):
        return str(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'email': self.email,
        }

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(120), unique=True, nullable=False)
    token_type = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime)
    expires = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User')

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    json_data = db.Column(db.JSON, nullable=False, default=dict())
    #join_code = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    user = db.relationship('User')



