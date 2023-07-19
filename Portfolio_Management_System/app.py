# app.py
# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/web22db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy database
db = SQLAlchemy(app)



# Import and register the blueprints for each entity's routes
from routes.portfolio_manager import portfolio_manager_bp
from routes.project import project_bp
from routes.task import task_bp
from routes.resource import resource_bp

app.register_blueprint(portfolio_manager_bp)
app.register_blueprint(project_bp)
app.register_blueprint(task_bp)
app.register_blueprint(resource_bp)

if __name__ == "__main__":
    # Create the database tables if they do not exist
    db.create_all()

    # Run the Flask application
    app.run(debug=True)