from . import db
from sqlalchemy import Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    profile_picture = Column(String(255), nullable=True)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    
    def check_password(self, password):
        """Check the hashed password."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Serialize user information (excluding password)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile_picture": self.profile_picture,
        }
