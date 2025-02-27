from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, get_current_user
from flask_cors import CORS

from backend.models import User, Chat
from backend.config import db
from backend.utils import add_token_to_database, revoke_token

profile = Blueprint('profile', __name__)
CORS(profile)


@profile.route('/profile', methods=["GET"], endpoint='profile_user')
@jwt_required()
def profile_user():
    current_user = get_current_user()
    if current_user:
        return jsonify({
            "nickname": current_user.nickname,
        }), 200
    return jsonify({
        "message": "User not found"
    }), 404

@profile.route('/chats', methods=["GET"], endpoint='load_chats')
@jwt_required()
def load_chats():
    chats_db = Chat.query.filter_by(user_id=get_jwt_identity()).all()
    chats = [{'id': i.id, 'name': 'Name of chat'} for i in chats_db]
    print(chats)
    return jsonify({
        'chats': chats
    })

@profile.route('/create_chat', methods=["GET"], endpoint='create_chat')
@jwt_required()
def create_chat():
    new_chat = Chat(user_id=get_jwt_identity())
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({
        'chat_id': str(new_chat.id),
    })

@profile.route('/load_chat/<chat_id>', methods=["GET"], endpoint='load_chat')
@jwt_required()
def load_chat(chat_id):
    chat = Chat.query.filter_by(id=chat_id).first()
    return jsonify({
        'data_messages': chat.json_data,
    })