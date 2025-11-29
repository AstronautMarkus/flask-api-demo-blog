from flask import request, jsonify
from app import db
from app.models import Task, User
from . import tasks_bp
from app.middlewares.auth_middleware import token_required

@tasks_bp.route('/', methods=['POST'])
@token_required # Add middleware here
def post_task(current_user_id):
    if not request.is_json:
        return jsonify({'error': 'Request body must be JSON.'}), 400
    data = request.json
    # Validate required fields and collect errors
    required_fields = ['title', 'user_id']
    errors = {}
    for field in required_fields:
        if field not in data or not data[field]:
            errors[field] = f'The field {field} is required.'
    # Validate user_id exists
    if 'user_id' in data and data.get('user_id'):
        if not User.query.get(data['user_id']):
            errors['user_id'] = 'The specified user_id does not exist.'
    if errors:
        return jsonify({'errors': errors}), 422
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        user_id=data['user_id']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully.', 'task': new_task.to_dict()}), 201
