from flask import request, jsonify, current_app
from app.models import RefreshToken
from . import auth_bp
import jwt
import datetime
from app import db

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    data = request.json
    refresh_token = data.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'Refresh token required.'}), 400

    token_obj = RefreshToken.query.filter_by(token=refresh_token, revoked=False).first()
    if not token_obj or token_obj.expires_at < datetime.datetime.utcnow():
        return jsonify({'error': 'Invalid or expired refresh token.'}), 401

    try:
        payload = jwt.decode(refresh_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Refresh token expired.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid refresh token.'}), 401

    # Generate new access token
    access_token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    return jsonify({'access_token': access_token}), 200
