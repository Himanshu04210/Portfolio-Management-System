from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the MySQL database URI with username and password
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/portfolio_management_system'

# Create the SQLAlchemy instance
db = SQLAlchemy(app)


# Define a model for the database table

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

# ...


# For portfolio manager


#Create a new managers
@app.route('/managers', methods=['POST'])
def create_portfolio_manager():
    data = request.json
    name = data.get('name')
    status = data.get('status')
    role = data.get('role')
    bio = data.get('bio')
    start_date = data.get('start_date')
    projects_data = data.get('projects')  # Assuming projects is a list of dictionaries

    if not all([name, status, role, start_date, projects_data]):
        return jsonify({"error": "Missing required fields"}), 400

    # Create the PortfolioManager instance
    portfolio_manager = PortfolioManager(name=name, status=status, role=role, bio=bio, start_date=start_date)
    
    if projects_data is not None:
        # Create or fetch the Project instances and associate them with the PortfolioManager
        projects = []
        for project_data in projects_data:
            project_name = project_data.get('project_name')
            status = project_data.get('status')
            start_date = project_data.get('start_date')
            end_date = project_data.get('end_date')
            project = Project(project_name=project_name, status=status, start_date=start_date, end_date=end_date)
            projects.append(project)
            db.session.add(project)

        # Assign the projects to the PortfolioManager
        portfolio_manager.projects.extend(projects)

    # Add the PortfolioManager to the database session and commit the changes
    db.session.add(portfolio_manager)
    db.session.commit()

    return jsonify({"message": "Manager with Projects created successfully!"}), 201


#Get all the manager
@app.route('/managers', methods=['GET'])
def get_all_portfolio_managers():
    portfolio_managers = PortfolioManager.query.all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "status": p.status,
        "role": p.role,
        "bio": p.bio,
        "start_date": p.start_date.isoformat()
    } for p in portfolio_managers])


#Get the manager by Id
@app.route('/managers/<int:portfolio_manager_id>', methods=['GET'])
def get_portfolio_manager_by_id(portfolio_manager_id):
    portfolio_manager = PortfolioManager.query.get(portfolio_manager_id)
    if not portfolio_manager:
        return jsonify({"error": "Portfolio Manager not found"}), 404
    return jsonify({
        "id": portfolio_manager.id,
        "name": portfolio_manager.name,
        "status": portfolio_manager.status,
        "role": portfolio_manager.role,
        "bio": portfolio_manager.bio,
        "start_date": portfolio_manager.start_date.isoformat()
    })




# for projects

@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.json
    project_name = data.get('project_name')
    status = data.get('status')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    portfolio_manager_id = data.get('portfolio_manager_id')

    if not all([project_name, status, start_date, portfolio_manager_id]):
        return jsonify({"error": "Missing required fields"}), 400

    project = Project(project_name=project_name, status=status, start_date=start_date, end_date=end_date, portfolio_manager_id=portfolio_manager_id)
    db.session.add(project)
    db.session.commit()
    return jsonify({"message": "Project created successfully!"})





@app.route('/projects', methods=['GET'])
def get_all_projects():
    projects = Project.query.all()
    return jsonify([{
        "id": p.id,
        "project_name": p.project_name,
        "status": p.status,
        "start_date": p.start_date.isoformat(),
        "end_date": p.end_date.isoformat() if p.end_date else None,
        "portfolio_manager_id": p.portfolio_manager_id
    } for p in projects])

@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project_by_id(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({
        "id": project.id,
        "project_name": project.project_name,
        "status": project.status,
        "start_date": project.start_date.isoformat(),
        "end_date": project.end_date.isoformat() if project.end_date else None,
        "portfolio_manager_id": project.portfolio_manager_id
    })

# Similarly, create GET methods for Task and Resource.



#for tasks


@app.route('/create_task', methods=['POST'])
def create_task():
    data = request.json
    name = data.get('name')
    status = data.get('status')
    project_id = data.get('project_id')

    if not all([name, status, project_id]):
        return jsonify({"error": "Missing required fields"}), 400

    task = Task(name=name, status=status, project_id=project_id)
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created successfully!"})



#for resources


@app.route('/create_resource', methods=['POST'])
def create_resource():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    task_id = data.get('task_id')

    if not all([name, task_id]):
        return jsonify({"error": "Missing required fields"}), 400

    resource = Resource(name=name, description=description, task_id=task_id)
    db.session.add(resource)
    db.session.commit()
    return jsonify({"message": "Resource created successfully!"})

# Define other CRUD methods for Resource using similar app.route decorators as above.








if __name__ == '__main__':
    with app.app_context():
        # Create the database tables
        db.create_all()
    app.run(debug=True)
