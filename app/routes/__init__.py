from .application_routes import application_blueprint
from .job_routes import main
from .user_routes import user_blueprint

__all__ = [
    'application_blueprint',
    'user_blueprint',
    'job_blueprint'
]