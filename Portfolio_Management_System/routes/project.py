from flask import Blueprint, jsonify, request
from app import db
from model import Project, PortfolioManager

project_bp = Blueprint('project', __name__, url_prefix='/project')

@project_bp.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    project_name = data.get('project_name')
    status = data.get('status')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    portfolio_manager_id = data.get('portfolio_manager_id')

    portfolio_manager = PortfolioManager.query.get(portfolio_manager_id)
    if not portfolio_manager:
        return jsonify({'error': 'Portfolio Manager not found'}), 404

    new_project = Project(project_name=project_name, status=status, start_date=start_date, end_date=end_date, portfolio_manager=portfolio_manager)
    db.session.add(new_project)
    db.session.commit()

    return jsonify({'message': 'Project created successfully'}), 201

@project_bp.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    result = [{'id': p.id, 'project_name': p.project_name, 'status': p.status, 'start_date': str(p.start_date), 'end_date': str(p.end_date), 'portfolio_manager_id': p.portfolio_manager_id} for p in projects]
    return jsonify(result), 200
