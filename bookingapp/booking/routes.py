## Endpoint Routes for Booking Blueprint
from flask import Blueprint, request, jsonify
from bookingapp.models.booking import Booking
from bookingapp import db
from bookingapp.utils.uuid_validation import IdSchema
from uuid import UUID

# Create the booking blueprint
booking_bp = Blueprint('booking', __name__, url_prefix='/api/v1/booking')

# test
@booking_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Booking Blueprint Working'}), 200