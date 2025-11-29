from flask import jsonify, request
from app import db
from app.models import Task
from . import tasks_bp

@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    # Pagination parameters
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        if page < 1 or per_page < 1 or per_page > 100:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid pagination parameters'}), 400

    pagination = Task.query.paginate(page=page, per_page=per_page, error_out=False)
    tasks = [task.to_dict() for task in pagination.items]
    response = {
        'tasks': tasks,
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

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    return jsonify(task.to_dict())
