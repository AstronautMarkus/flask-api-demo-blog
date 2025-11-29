from flask import request, jsonify
from app import db
from app.models import Task, User
from datetime import datetime
from . import tasks_bp

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def put_task(task_id):
    if not request.is_json:
        return jsonify({'error': 'Request body must be JSON.'}), 400
    data = request.json
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found.'}), 404
    errors = {}
    # Validate user_id exists if being updated
    if 'user_id' in data and data.get('user_id'):
        if not User.query.get(data['user_id']):
            errors['user_id'] = 'The specified user_id does not exist.'
    if errors:
        return jsonify({'errors': errors}), 422
    # Update task fields
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    task.date_completed = datetime.utcnow() if task.completed else None
    if 'user_id' in data and data.get('user_id'):
        task.user_id = data['user_id']
    db.session.commit()
    return jsonify({'message': 'Task updated successfully.', 'task': task.to_dict()}), 200
