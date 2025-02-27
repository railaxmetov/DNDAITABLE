from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_refresh_token, create_access_token, get_jwt, get_current_user
from flask_cors import CORS

from werkzeug.security import check_password_hash, generate_password_hash

from backend.models import User
from backend.config import db
from backend.utils import add_token_to_database, revoke_token

auth = Blueprint('auth', __name__)
CORS(auth)

@auth.route('/login', methods=["POST"])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        ###login_user(user, remember=True if request.json.get('rememberMe') else False)
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        add_token_to_database(access_token)
        add_token_to_database(refresh_token)
        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token,
        ), 200

    return jsonify({
        "message": "Invalid email or password."
    }), 500


@auth.route('/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    add_token_to_database(access_token)
    return jsonify(
        access_token=access_token
    ), 200


@auth.route('/revoke_access', methods=['DELETE'])
@jwt_required()
def revoke_access_token():
    jti = get_jwt()['jti']
    user_id = get_jwt_identity()
    revoke_token(jti, user_id)
    return jsonify({}), 200


@auth.route('/revoke_refresh', methods=['DELETE'])
@jwt_required(refresh=True)
def revoke_refresh_token():
    jti = get_jwt()['jti']
    user_id = get_jwt_identity()
    revoke_token(jti, user_id)
    return jsonify({}), 200



@auth.route('/fastlogin', methods=["GET"])
@jwt_required()
def fast_login():
    user_id = get_jwt_identity()
    if user_id:
        print('Fast logged in')
        access_token = create_access_token(identity=user_id)
        add_token_to_database(access_token)
        return jsonify(
            access_token=access_token,
        ), 200
    return jsonify({}), 304


@auth.route('/regist', methods=["POST"])
def regist():
    nickname = request.json.get("nickname")
    email = request.json.get("email")
    password = request.json.get("password")
    repeat_password = request.json.get("repeatPassword")

    if password == repeat_password:
        hash_password = generate_password_hash(password)
        if not User.query.filter_by(email=email).first():
            db.session.add(User(nickname=nickname, email=email, password=hash_password))
            db.session.commit()
            return jsonify({}), 200
        else:
            return jsonify({
                "message": "Email already in use"
            }), 404
    else:
        return jsonify({
            "message": "Incorrect password repeat"
        }), 400


