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

@users_bp.route('/', methods=['POST'])
def post_user():

    if not request.is_json:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    data = request.json

    # Validate required fields and collect errors
    required_fields = ['username', 'email', 'password', 'confirm_password']
    errors = {}
    for field in required_fields:
        if field not in data or not data[field]:
            errors[field] = f'The field {field} is required.'

    # Validate password confirmation
    if 'password' in data and 'confirm_password' in data:
        if data['password'] != data['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match.'

    # Validate password security
    if 'password' in data and data.get('password'):
        secure, msg = is_password_secure(
            data['password'],
            min_length=8,      # Modify this as needed
            max_length=32,
            allowed_chars=r'^[A-Za-z0-9@#$%^&+=]*$'
        )
        if not secure:
            errors['password'] = msg

    # Validate email uniqueness
    if 'email' in data and data.get('email'):
        if User.query.filter_by(email=data['email']).first():
            errors['email'] = 'The email is already registered.'

    if errors:
        return jsonify({'errors': errors}), 422

    # Encrypt password and create user
    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully.', 'user': new_user.to_dict()}), 201
