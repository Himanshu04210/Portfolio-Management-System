# models.py
from app import db

class PortfolioManager(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, autoincrement=True)
    status = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)

    # One-to-Many relationship with projects
    projects = db.relationship('Project', backref='portfolio_manager', lazy=True)   

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    # Many-to-One relationship with PortfolioManager
    portfolio_manager_id = db.Column(db.Integer, db.ForeignKey('portfolio_manager.id'), nullable=False)

    # One-to-Many relationship with tasks
    tasks = db.relationship('Task', backref='project', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    # Many-to-One relationship with Project
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    # One-to-Many relationship with resources
    resources = db.relationship('Resource', backref='task', lazy=True)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    # Many-to-One relationship with Task
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
