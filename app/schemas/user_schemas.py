from marshmallow import Schema, fields, validate

# Define Marshmallow Schema for User validation
class UserRegistrationSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    email = fields.Email(required=True, validate=validate.Length(min=5, max=255))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=8, max=128))
    profile_picture = fields.String(required=False, validate=validate.Length(max=255))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)



