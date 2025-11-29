from flask import Blueprint
tasks_bp = Blueprint('tasks', __name__)

from . import get_tasks
from . import post_task
from . import put_task
from . import delete_task
