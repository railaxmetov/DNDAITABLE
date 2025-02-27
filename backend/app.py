from backend.config import app, db, socketio, jwt
from blueprints.auth import auth
from blueprints.profile import profile

# Допы для дополнительной настройки jwt через декораторы
from utils import is_token_revoked
from backend.models import User

# настройка jwt
@app.teardown_appcontext
def close_db(error):
    db.session.close()

@jwt.token_in_blocklist_loader
def check_is_token_revoked(jwt_headers, jwt_payload):
    try:
        return is_token_revoked(jwt_payload)
    except Exception:
        return True

@jwt.user_lookup_loader
def load_user(jwt_headers, jwt_payload):
    user_id = jwt_payload['user_id']
    return User.query.filter_by(id=user_id).first()
app.register_blueprint(auth)
app.register_blueprint(profile)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app=app, debug=True, allow_unsafe_werkzeug=True)
