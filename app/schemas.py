from marshmallow import Schema, fields, validate

# Define Marshmallow Schema for Job Validation
class JobSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    company = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    location = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=True, validate=lambda x: len(x) > 0)
    salary = fields.Str()
    employment_type = fields.Str()
    application_deadline = fields.DateTime()
    skills_required = fields.Str()
    date_posted = fields.DateTime(dump_only=True)

