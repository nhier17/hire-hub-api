from dotenv import load_dotenv
import os

load_dotenv()

postgres_uri = os.getenv('POSTGRESQL_URI')

if not postgres_uri:
    raise ValueError("No 'POSTGRESQL_URI' set for Flask application. Please set it in the .env file.")

class Config:
    SQLALCHEMY_DATABASE_URI = postgres_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    
    # File Upload Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
    UPLOAD_EXTENSIONS = ['.pdf', '.doc', '.docx']
    UPLOAD_PATH = 'uploads/resumes'

    @staticmethod
    def ensure_upload_path_exists():
        if not os.path.exists(Config.UPLOAD_PATH):
            os.makedirs(Config.UPLOAD_PATH)

Config.ensure_upload_path_exists()
