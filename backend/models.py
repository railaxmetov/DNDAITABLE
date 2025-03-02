from email.policy import default

from backend.config import db
import random
import string
import copy

def generate_join_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    chats = db.relationship(
        'Chat',
        secondary='user_chat_association',
        back_populates='users'
    )

    def get_id(self):
        return str(self.id)

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(120), unique=True, nullable=False)
    token_type = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime)
    expires = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User')

class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    json_data = db.Column(db.JSON, nullable=False, default={'chat': []})
    join_code = db.Column(db.String(8), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    def __init__(self, user_id):
        self.join_code = generate_join_code()
        self.user_id = user_id

    users = db.relationship(
        'User',
        secondary='user_chat_association',
        back_populates='chats'
    )

    def insert_json_data(self, data):
        old_data = copy.deepcopy(self.json_data)
        data['id'] = len(old_data['chat'])
        old_data['chat'].append(data)
        self.json_data = old_data
        db.session.commit()


class UserChatAssociation(db.Model):
    __tablename__ = 'user_chat_association'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False, index=True)

    user = db.relationship('User', backref='user_chats')
    chat = db.relationship('Chat', backref='chat_users')




