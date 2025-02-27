from datetime import datetime

from flask_jwt_extended import decode_token

from backend.models import TokenBlocklist
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