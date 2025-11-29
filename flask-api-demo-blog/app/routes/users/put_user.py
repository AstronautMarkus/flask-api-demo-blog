from flask import request, jsonify
from app import db
from app.models import User
from . import users_bp
import re
from werkzeug.security import generate_password_hash

def is_password_secure(password, min_length=8, max_length=32, allowed_chars=r'^[A-Za-z0-9@#$%^&+=]*$'):
    """
    Check if the password meets security requirements.
    - min_length: minimum length
    - max_length: maximum length
    - allowed_chars: regex of allowed characters
    """
    if not isinstance(password, str):
        return False, 'Password must be a string.'
    if len(password) < min_length:
        return False, f'Password must be at least {min_length} characters.'
    if len(password) > max_length:
        return False, f'Password must be at most {max_length} characters.'
    if not re.match(allowed_chars, password):
        return False, 'Password contains invalid characters.'
    return True, None

@users_bp.route('/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    if not request.is_json:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    data = request.json
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    errors = {}

    # Validate email uniqueness if email is being updated
    if 'email' in data and data.get('email') and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            errors['email'] = 'The email is already registered.'

    # Validate password security if password is being updated
    if 'password' in data and data.get('password'):
        secure, msg = is_password_secure(
            data['password'],
            min_length=8,
            max_length=32,
            allowed_chars=r'^[A-Za-z0-9@#$%^&+=]*$'
        )
        if not secure:
            errors['password'] = msg

    if errors:
        return jsonify({'errors': errors}), 422

    # Update user fields
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)

    # Encrypt password if it's being updated
    if 'password' in data and data.get('password'):
        user.password = generate_password_hash(data['password'])

    db.session.commit()
    return jsonify({'message': 'User updated successfully.', 'user': user.to_dict()}), 200
