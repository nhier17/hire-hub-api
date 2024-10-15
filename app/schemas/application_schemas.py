from marshmallow import Schema, fields, validate, validates, ValidationError
from .user_schemas import UserRegistrationSchema
from .job_schemas import JobSchema

class ApplicationCreateSchema(Schema):
    job_id = fields.Integer(required=True)
    cover_letter = fields.String(required=False, allow_none=True, validate=validate.Length(max=2000))
    
    @validates('job_id')
    def validate_job_id(self, value):
        from app.models import Job
        if not Job.query.get(value):
            raise ValidationError('Job with the given ID does not exist.')

class ApplicationResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    user = fields.Nested(UserRegistrationSchema, dump_only=True)
    job = fields.Nested(JobSchema, dump_only=True)
    date_applied = fields.DateTime(dump_only=True)
    cover_letter = fields.String(allow_none=True)
