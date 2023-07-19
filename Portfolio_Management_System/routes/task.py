from flask import Blueprint, jsonify, request
from app import db
from model import Task, Project

task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    name = data.get('name')
    status = data.get('status')
    project_id = data.get('project_id')

    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    new_task = Task(name=name, status=status, project=project)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully'}), 201

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    result = [{'id': t.id, 'name': t.name, 'status': t.status, 'project_id': t.project_id} for t in tasks]
    return jsonify(result), 200
