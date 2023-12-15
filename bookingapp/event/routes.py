# events/routes.py

from flask import Blueprint, request, jsonify, abort
from flask_login import current_user
from bookingapp.models.event import Event
from bookingapp import db, app
from bookingapp.utils.uuid_validation import IdSchema
from uuid import UUID

# Create the event blueprint
event_bp = Blueprint('event', __name__, url_prefix='/api/v1/event')

# Decorator for Admin-Only Access
def admin_only(func):
    def wrapper(*args, **kwargs):
        # Check if the user is logged in and has the 'admin' role
        if current_user.is_authenticated and current_user.role == 'admin':
            return func(*args, **kwargs)
        else:
            abort(403)  # Forbidden
    return wrapper


# Input Validation using marshmallow
class EventSchema(ma.Schema):
    class Meta:
        fields = ('name', 'date', 'location', 'description')

event_schema = EventSchema()

# Endpoint for Admin-Only Event Creation
@event_bp.route('/', methods=['POST'])
@admin_only
def create_event():
    # Input validation using Marshmallow
    data = request.json
    errors = event_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    # ORM query to create an event
    new_event = Event(**data)
    db.session.add(new_event)
    db.session.commit()

    return jsonify(message='Event created successfully'), 201

# Endpoint for Update Event (PUT/PATCH)
@event_bp.route('/<uuid:event_id>', methods=['PUT', 'PATCH'])
@admin_only
def update_event(event_id):
    # Input validation using Marshmallow
    data = request.json
    errors = event_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    # ORM query to update an event
    event = Event.query.get_or_404(UUID(event_id))
    event.name = data['name']
    event.date = data['date']
    event.location = data['location']
    event.description = data['description']

    db.session.commit()

    return jsonify(message='Event updated successfully'), 200

# Endpoint for Delete Event
@event_bp.route('/<uuid:event_id>', methods=['DELETE'])
@admin_only
def delete_event(event_id):
    # Input validation for UUID
    schema = IdSchema()
    errors = schema.validate({'id': event_id})
    if errors:
        return jsonify({'errors': errors}), 400

    # ORM query to delete an event
    event = Event.query.get_or_404(UUID(event_id))
    db.session.delete(event)
    db.session.commit()

    return jsonify(message='Event deleted successfully'), 200

# Endpoint for Testing
@event_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Event Blueprint Working'}), 200

