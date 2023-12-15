from marshmallow import Schema, fields, ValidationError

class IdSchema(Schema):
    id = fields.UUID(required=True)

def validate_uuid(value):
    try:
        schema = IdSchema()
        result = schema.load({'id': value})
        return result['id']
    except ValidationError as e:
        raise ValueError(f"Invalid UUID format: {e.messages}")
