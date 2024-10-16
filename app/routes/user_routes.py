from flask import Blueprint, jsonify, request
from .. import db
from ..models import User
from ..schemas import UserRegistrationSchema, UserLoginSchema
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token
from datetime import timedelta


user_blueprint = Blueprint('users', __name__)

registration_schema = UserRegistrationSchema()
login_schema = UserLoginSchema()

@user_blueprint.route('/api/auth/register', methods=['POST'])
def register():
    """
    Register a new user and return a JWT access token along with user information.
    """
    try:
        # Parse and validate input
        data = request.get_json()
        user_data = registration_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=user_data['email']).first()
    if existing_user:
        return jsonify({"message": "User with this email already exists."}), 400

    # Create new user instance
    new_user = User(
        name=user_data['name'],
        email=user_data['email'],
        profile_picture=user_data.get('profile_picture')
    )
    new_user.set_password(user_data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Database Integrity Error."}), 500

    # Create a JWT token for the new user
    access_token = create_access_token(identity={"user_id": new_user.id}, expires_delta=timedelta(days=1))

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "profile_picture": new_user.profile_picture
        }
    }), 201


@user_blueprint.route('/api/auth/login', methods=['POST'])
def login():
    """
    Authenticate a user and return a JWT.
    """
    try:
        # Parse and validate input
        data = request.get_json()
        login_data = login_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    # Fetch user by email
    user = User.query.filter_by(email=login_data['email']).first()
    if not user or not user.check_password(login_data['password']):
        return jsonify({"message": "Invalid credentials."}), 401

    # Create JWT token
    access_token = create_access_token(identity={"user_id":user.id}, expires_delta=timedelta(days=1))

    return jsonify({"access_token": access_token,
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "profile_picture": user.profile_picture
                    }
                     }), 200
