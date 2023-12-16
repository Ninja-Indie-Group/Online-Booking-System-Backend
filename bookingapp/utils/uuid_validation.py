from marshmallow import Schema, fields, ValidationError
from uuid import UUID, uuid4

class IdSchema(Schema):
    id = fields.UUID(required=True)

def validate_uuid(value):
    try:
        schema = IdSchema()
        result = schema.load({'id': value})
        return str(result['id'])  # Convert UUID to string
    except ValidationError as e:
        raise ValueError(f"Invalid UUID format: {e.messages}")