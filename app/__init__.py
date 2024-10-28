from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
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
    from .models import Job, User, Application


    # Enable CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize Swagger for API documentation
    swagger = Swagger(app)

    # Register blueprints 
    from .routes import main as main_blueprint, user_blueprint, application_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(application_blueprint)

    @app.route('/')
    def index():
        return jsonify({
            "message": "Welcome to HireHub API",
            "documentation": "Visit /apidocs for API documentation."
        })




    return app
