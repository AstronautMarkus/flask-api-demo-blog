from flask import request, jsonify, current_app
from app.models import User, RefreshToken
from . import auth_bp
from werkzeug.security import check_password_hash
import jwt
import datetime
from app import db

def generate_tokens(user_id):
    access_token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    refresh_exp = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    refresh_token = jwt.encode({
        'user_id': user_id,
        'exp': refresh_exp
    }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    # Store refresh token in DB
    new_refresh = RefreshToken(
        user_id=user_id,
        token=refresh_token,
        created_at=datetime.datetime.utcnow(),
        expires_at=refresh_exp,
        revoked=False
    )
    db.session.add(new_refresh)
    db.session.commit()

    return access_token, refresh_token

@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Request body must be JSON.'}), 400
    data = request.json

    # Validate required fields and collect errors
    required_fields = ['email', 'password']
    errors = {}
    for field in required_fields:
        if field not in data or not data[field]:
            errors[field] = f'The field {field} is required.'

    if errors:
        return jsonify({'errors': errors}), 422

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid email or password.'}), 401

    access_token, refresh_token = generate_tokens(user.id)
    return jsonify({
        'message': 'Login successful.',
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200
