## Endpoint Routes for venue Blueprint
from flask import Blueprint, request, jsonify
from bookingapp.models.venue import Venue
from bookingapp import db
from bookingapp.utils.uuid_validation import IdSchema
from uuid import UUID

# Create the venue blueprint
venue_bp = Blueprint('venue', __name__, url_prefix='/api/v1/venue')

# test
@venue_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Venue Blueprint Working'}), 200