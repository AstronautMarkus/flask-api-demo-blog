from flask import jsonify, request
from app import db
from app.models import User
from . import users_bp
from app.middlewares.auth_middleware import token_required

@users_bp.route('/', methods=['GET'])
def get_users():
    # Pagination parameters
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        if page < 1 or per_page < 1 or per_page > 100:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid pagination parameters'}), 400

    pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
    users = [user.to_dict() for user in pagination.items]
    response = {
        'users': users,
        'pagination': {
            'total': pagination.total,
            'pages': pagination.pages,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }
    return jsonify(response)

@users_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user_id, user_id):
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized access.'}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.to_dict())
