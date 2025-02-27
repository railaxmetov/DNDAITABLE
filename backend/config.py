from datetime import timedelta
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_socketio import SocketIO, emit
from flask_cors import CORS

import os
from environs import env


env.read_env('../.env')
app = Flask(__name__)
CORS(app)

# Секретный ключ
app.config['SECRET_KEY'] = env.str('SECRET_KEY')

# База данных бэка
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Менеджер джаваскрипт веб токенов
app.config["JWT_SECRET_KEY"] = env.str('SECRET_KEY')
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_IDENTITY_CLAIM"] = "user_id"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(weeks=10)
jwt = JWTManager(app)

# Вебсокет
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def connect():
    print(f'Client connected: {request.sid}')

@socketio.on('data')
def data_handler(data):
    emit('data', {'socketID': request.sid, 'data': data}, broadcast=True)


@socketio.on('disconnect')
def disconnect():
    print(f'Client disconnected: {request.sid}')