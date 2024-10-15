from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # import models
    from .models.job_model import Job
    from .models.user_model import User
    from .models.application_model import Application

    # Enable CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints 
    from .routes.job_routes import main as main_blueprint
    from .routes.user_routes import user_blueprint
    from .routes.application_routes import application_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(application_blueprint)


    return app
