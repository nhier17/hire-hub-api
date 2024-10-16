from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
import os

from .. import db
from ..models import Application, Job
from ..schemas import ApplicationCreateSchema, ApplicationResponseSchema

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
        # Validate form data
        form = request.form.to_dict()
        application_data = application_create_schema.load(form)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    # Handle resume upload
    if 'resume' not in request.files:
        return jsonify({"message": "Resume file is required."}), 400

    resume = request.files['resume']
    if resume.filename == '':
        return jsonify({"message": "No selected file."}), 400

    filename = secure_filename(resume.filename)
    file_ext = os.path.splitext(filename)[1].lower()

    if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
        return jsonify({"message": "Invalid file type."}), 400

    resume_path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
    resume.save(resume_path)

    # Get current user ID
    current_user_id = get_jwt_identity()['user_id']
    job_id = application_data['job_id']

    # Check if job exists
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"message": "Job not found"}), 404

    # Check if the user has already applied for this job
    existing_application = Application.query.filter_by(user_id=current_user_id, job_id=job_id).first()
    if existing_application:
        return jsonify({"message": "You have already applied for this job"}), 400

    # Create new application
    new_application = Application(
        user_id=current_user_id,
        job_id=job_id,
        full_name=application_data['full_name'],
        email=application_data['email'],
        phone_number=application_data['phone_number'],
        resume=resume_path,
        portfolio=application_data.get('portfolio'),
        country_of_residence=application_data['country_of_residence'],
        notice_period=application_data['notice_period'],
        salary_expectation=application_data['salary_expectation'],
        years_of_experience=application_data['years_of_experience'],
        cover_letter=application_data.get('cover_letter')
    )

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
