from datetime import datetime

from flask_jwt_extended import decode_token
from flask_socketio import emit, leave_room, join_room
from flask import request

from backend.models import TokenBlocklist, User, Chat
from backend.config import db


def add_token_to_database(encoded_token):
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_id = decoded_token['user_id']
    expires = datetime.fromtimestamp(decoded_token['exp'])

    db_token = TokenBlocklist(
        jti=jti,
        user_id=user_id,
        expires=expires,
        token_type=token_type,

    )
    db.session.add(db_token)
    db.session.commit()


def revoke_token(token_jti, user_id):
    try:
        token = TokenBlocklist.query.filter_by(jti=token_jti, user_id=user_id).one()
        token.revoked_at = datetime.utcnow()
        db.session.commit()
    except Exception as e:
        print(f'Could not revoke token: {token_jti}, error: {e}')


def is_token_revoked(jwt_payload):
    token_jti = jwt_payload['jti']
    user_id = jwt_payload['user_id']
    try:
        token = TokenBlocklist.query.filter_by(jti=token_jti, user_id=user_id).one()
        return token.revoked_at is not None
    except Exception as e:
        print(f'Could not revoke token: {token_jti}, error: {e}')


# Настройка вебсокета
class ChatServer:
    def __init__(self, app, socketio):
        self.app = app
        self.socketio = socketio
        self.chats = {}  # {chat_id: set(user_ids)}
        self.db_chats = {}

        self.socketio.on_event('connect', self.handle_connect)
        self.socketio.on_event('join', self.handle_join)
        self.socketio.on_event('leave', self.handle_leave)
        self.socketio.on_event('message', self.handle_message)

    def handle_connect(self):
        print(f'Client connected: {request.sid}')

    def handle_join(self, data):
        user_id = data.get('user_id')
        chat_id = data.get('chat_id')

        if not user_id or not chat_id:
            return

        if chat_id not in self.chats:
            self.chats[chat_id] = set()
            self.db_chats[chat_id] = Chat.query.filter_by(id=chat_id).first()

        self.chats[chat_id].add(user_id)
        join_room(chat_id)

        emit('message', {'message': f'{User.query.filter_by(id=user_id).first().nickname} joined chat',
                         'nickname': 'System'}, to=chat_id, broadcast=True)

    def handle_leave(self, data):
        user_id = data.get('user_id')
        chat_id = data.get('chat_id')

        if not user_id or not chat_id:
            return

        if chat_id in self.chats and user_id in self.chats[chat_id]:
            self.chats[chat_id].remove(user_id)
            leave_room(chat_id)

            emit('message', {'message': f'{User.query.filter_by(id=user_id).first().nickname} left chat',
                             'nickname': 'System'}, to=chat_id, broadcast=True)

        if not self.chats[chat_id]:
            del(self.chats[chat_id])
            del(self.db_chats[chat_id])

    def handle_message(self, data):
        user_id = data.get('user_id')
        chat_id = data.get('chat_id')
        message = data.get('message')

        if not user_id or not chat_id or not message:
            return

        res_data = {'message': message, 'nickname': User.query.filter_by(id=user_id).first().nickname}
        emit('message', res_data, to=chat_id, broadcast=True)
        cur_chat = Chat.query.filter_by(id=chat_id).first()
        cur_chat.insert_json_data(res_data)

    def run(self, host, port, debug, allow_unsafe_werkzeug):
        self.socketio.run(self.app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=allow_unsafe_werkzeug)

