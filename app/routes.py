from flask import Blueprint, jsonify, request, abort
from . import db
from .models import Job
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields, ValidationError
from sqlalchemy import text

main = Blueprint('main', __name__)

# Define Marshmallow Schema for Job Validation
class JobSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=lambda x: len(x) > 0)
    company = fields.Str(required=True, validate=lambda x: len(x) > 0)
    location = fields.Str(required=True, validate=lambda x: len(x) > 0)
    description = fields.Str(required=True, validate=lambda x: len(x) > 0)
    salary = fields.Str()
    employment_type = fields.Str()
    application_deadline = fields.DateTime()
    skills_required = fields.Str()
    date_posted = fields.DateTime(dump_only=True)

job_schema = JobSchema()
jobs_schema = JobSchema(many=True)

@main.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.is_json:
        abort(400, description="Request must be JSON")
    try:
        data = request.get_json()
        job_data = job_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    job = Job(
        title=job_data['title'],
        company=job_data['company'],
        location=job_data['location'],
        description=job_data['description'],
        salary=job_data.get('salary'),
        employment_type=job_data.get('employment_type'),
        application_deadline=job_data.get('application_deadline'),
        skills_required=job_data.get('skills_required'),
        date_posted=datetime.now(timezone.utc)  # Automatically set to current UTC time
    )
    try:
        db.session.add(job)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(500, description="Database integrity error")
    
    return job_schema.dump(job), 201  # Use dump instead of jsonify

@main.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.order_by(Job.date_posted.desc()).all()
    return jobs_schema.dump(jobs), 200  # Use dump instead of jsonify

@main.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id, description=f"Job with id {job_id} not found")
    return job_schema.dump(job), 200  # Use dump instead of jsonify

@main.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get_or_404(job_id, description=f"Job with id {job_id} not found")
    if not request.is_json:
        abort(400, description="Request must be JSON")
    try:
        data = request.get_json()
        # Prevent clients from modifying 'date_posted'
        if 'date_posted' in data:
            abort(400, description="Cannot modify 'date_posted' field")
        job_data = job_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    for key, value in job_data.items():
        setattr(job, key, value)
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(500, description="Database integrity error")
    
    return job_schema.dump(job), 200  # Use dump instead of jsonify

@main.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id, description=f"Job with id {job_id} not found")
    try:
        db.session.delete(job)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(500, description="Database integrity error")
    return jsonify({'message': 'Job deleted successfully'}), 200

@main.route('/api/test_db', methods=['GET'])
def test_connection():
    try:
        # Obtain a connection from the database engine
        with db.engine.connect() as connection:
            # Execute the SQL query
            result = connection.execute(text("SELECT 1"))
            # Fetch the result (optional)
            result_value = result.fetchone()
            return jsonify({"message": "Connection successful!", "result": result_value[0]}), 200
    except Exception as e:
        return jsonify({"error": str(e), "message": "Connection failed!"}), 500

# Custom Error Handlers
@main.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': error.description}), 400

@main.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': error.description}), 404

@main.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': error.description}), 500
