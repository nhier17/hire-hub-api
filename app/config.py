import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)


postgres_uri = os.getenv('POSTGRESQL_URI')

if not postgres_uri:
    raise ValueError("No 'POSTGRESQL_URI' set for Flask application. Please set it in the .env file.")

class Config:
    SQLALCHEMY_DATABASE_URI = postgres_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
