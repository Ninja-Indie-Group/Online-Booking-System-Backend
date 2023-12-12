## Endpoint Routes for Event Blueprint
from flask import Blueprint, request, jsonify
from bookingapp.models.event import Event
from bookingapp import db
from bookingapp.utils.uuid_validation import IdSchema
from uuid import UUID

# Create the event blueprint
event_bp = Blueprint('event', __name__, url_prefix='/api/v1/event')

# test
@event_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Event Blueprint Working'}), 200