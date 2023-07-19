# routes/portfolio_manager.py
from flask import Blueprint, jsonify, request
from app import db
from model import PortfolioManager

# Create the blueprint object
portfolio_manager_bp = Blueprint('portfolio_manager', __name__, url_prefix='/portfolio_manager')

# Define your portfolio_manager routes and handlers here
# For example:
@portfolio_manager_bp.route('/managers', methods=['POST'])
def create_portfolio_manager():
    data = request.get_json()
    name = data.get('name')
    status = data.get('status')
    role = data.get('role')
    bio = data.get('bio')
    start_date = data.get('start_date')

    new_portfolio_manager = PortfolioManager(name=name, status=status, role=role, bio=bio, start_date=start_date)
    db.session.add(new_portfolio_manager)
    db.session.commit()

    return jsonify({'message': 'Portfolio Manager created successfully'}), 201

@portfolio_manager_bp.route('/managers', methods=['GET'])
def get_portfolio_managers():
    portfolio_managers = PortfolioManager.query.all()
    result = [{'id': p.id, 'name': p.name, 'status': p.status, 'role': p.role, 'bio': p.bio, 'start_date': str(p.start_date)} for p in portfolio_managers]
    return jsonify(result), 200
