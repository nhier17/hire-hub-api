from flask import Blueprint, jsonify, request, abort
from .. import db
from ..models import Job
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from ..schemas import JobSchema
from sqlalchemy import text
from marshmallow import ValidationError
from flasgger import swag_from

main = Blueprint('main', __name__)

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
        date_posted=datetime.now(timezone.utc) 
    )
    try:
        db.session.add(job)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(500, description="Database integrity error")
    
    return job_schema.dump(job), 201 

@main.route('/api/jobs', methods=['GET'])
@swag_from({
    'parameters': [
        {'name': 'search', 'in': 'query', 'type': 'string', 'description': 'Job title or keyword'},
        {'name': 'location', 'in': 'query', 'type': 'string', 'description': 'Location to filter jobs by'},
        {'name': 'page', 'in': 'query', 'type': 'integer', 'default': 1, 'description': 'Pagination page number'},
        {'name': 'per_page', 'in': 'query', 'type': 'integer', 'default': 10, 'description': 'Items per page'}
    ],
    'responses': {
        200: {
            'description': 'List of job results',
            'examples': {
                'application/json': {
                    'jobs': [{'id': 1, 'title': 'Software Engineer'}],
                    'total': 100,
                    'pages': 10,
                    'current_page': 1
                }
            }
        }
    }
})
def get_jobs():
    search = request.args.get('search', '', type=str)
    location = request.args.get('location', '', type=str)
    company = request.args.get('company', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Job.query

    if search:
        query = query.filter(Job.title.ilike(f'%{search}%'))
    
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))
    
    if company:
        query = query.filter(Job.company.ilike(f'%{company}%'))
    
    jobs_pagination = query.order_by(Job.date_posted.desc()).paginate(page=page, per_page=per_page, error_out=False)
    jobs = jobs_pagination.items

    return jsonify({
        'jobs': jobs_schema.dump(jobs),
        'total': jobs_pagination.total,
        'pages': jobs_pagination.pages,
        'current_page': jobs_pagination.page
    }), 200



@main.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id, description=f"Job with id {job_id} not found")
    return job_schema.dump(job), 200  

@main.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get_or_404(job_id, description=f"Job with id {job_id} not found")
    if not request.is_json:
        abort(400, description="Request must be JSON")
    try:
        data = request.get_json()
        
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
    
    return job_schema.dump(job), 200  

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
