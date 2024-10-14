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

# Define Marshmallow Schema for User validation
class UserRegistrationSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    email = fields.Email(required=True, validate=validate.Length(min=5, max=255))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=8, max=128))
    profile_picture = fields.String(required=False, validate=validate.Length(max=255))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)



