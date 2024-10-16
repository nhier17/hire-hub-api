from marshmallow import Schema, fields, validate, validates, ValidationError
from .user_schemas import UserRegistrationSchema
from .job_schemas import JobSchema

class ApplicationCreateSchema(Schema):
    job_id = fields.Integer(required=True)
    full_name = fields.String(required=True, validate=validate.Length(max=100))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    phone_number = fields.String(required=True, validate=validate.Length(max=20))
    resume = fields.Raw(required=True)  # For file uploads
    portfolio = fields.String(required=False, validate=validate.Length(max=255))
    country_of_residence = fields.String(required=True, validate=validate.Length(max=100))
    notice_period = fields.Integer(required=True, validate=validate.Range(min=0))
    salary_expectation = fields.Integer(required=True, validate=validate.Range(min=0))
    years_of_experience = fields.Integer(required=True, validate=validate.Range(min=0))
    cover_letter = fields.String(required=False, allow_none=True, validate=validate.Length(max=2000))
    
    @validates('job_id')
    def validate_job_id(self, value):
        from app.models.job_model import Job
        if not Job.query.get(value):
            raise ValidationError('Job with the given ID does not exist.')

class ApplicationResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    user = fields.Nested(UserRegistrationSchema, dump_only=True)
    job = fields.Nested(JobSchema, dump_only=True)
    full_name = fields.String()
    email = fields.Email()
    phone_number = fields.String()
    resume = fields.String()
    portfolio = fields.String()
    country_of_residence = fields.String()
    notice_period = fields.Integer()
    salary_expectation = fields.Integer()
    years_of_experience = fields.Integer()
    date_applied = fields.DateTime()
    cover_letter = fields.String()
