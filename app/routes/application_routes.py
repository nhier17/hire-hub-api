from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from .. import db
from ..models.application_model import Application
from ..schemas.application_schemas import ApplicationCreateSchema, ApplicationResponseSchema

application_blueprint = Blueprint('applications', __name__)

application_create_schema = ApplicationCreateSchema()
application_response_schema = ApplicationResponseSchema()
applications_response_schema = ApplicationResponseSchema(many=True)

@application_blueprint.route('/api/apply', methods=['POST'])
@jwt_required()
def apply_for_job():
    """
    Apply for a job.
    """
    try:
        # Parse and validate input
        data = request.get_json()
        application_data = application_create_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    current_user_id = get_jwt_identity()['user_id']
    job_id = application_data['job_id']
    cover_letter = application_data.get('cover_letter', '')

    # Check if job exists
    job = db.session.query(Application.job).filter(Application.job_id == job_id).first()
    if not job:
        return jsonify({"message": "Job not found"}), 404

    # Check if the user has already applied for this job
    existing_application = Application.query.filter_by(user_id=current_user_id, job_id=job_id).first()
    if existing_application:
        return jsonify({"message": "You have already applied for this job"}), 400

    # Create new application
    new_application = Application(user_id=current_user_id, job_id=job_id, cover_letter=cover_letter)

    try:
        db.session.add(new_application)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Database Integrity Error."}), 500

    result = application_response_schema.dump(new_application)
    return jsonify({"message": "Application submitted successfully", "application": result}), 201

@application_blueprint.route('/api/applications', methods=['GET'])
@jwt_required()
def get_user_applications():
    """
    Get all applications for the logged-in user.
    """
    current_user_id = get_jwt_identity()['user_id']
    applications = Application.query.filter_by(user_id=current_user_id).all()
    result = applications_response_schema.dump(applications)
    return jsonify(result), 200
