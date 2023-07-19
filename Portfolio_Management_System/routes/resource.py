from flask import Blueprint, jsonify, request
from app import db
from model import Resource, Task

resource_bp = Blueprint('resource', __name__, url_prefix='/resource')

@resource_bp.route('/resources', methods=['POST'])
def create_resource():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    task_id = data.get('task_id')

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    new_resource = Resource(name=name, description=description, task=task)
    db.session.add(new_resource)
    db.session.commit()

    return jsonify({'message': 'Resource created successfully'}), 201

@resource_bp.route('/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    result = [{'id': r.id, 'name': r.name, 'description': r.description, 'task_id': r.task_id} for r in resources]
    return jsonify(result), 200
