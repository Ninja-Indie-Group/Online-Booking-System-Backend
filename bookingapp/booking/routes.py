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

# Route to Get all Bookings of an event
@booking_bp.route('/<event_id>', methods=['GET'])
def get_bookings(event_id):
    """
    Retrieves the bookings for a specific event.

    Parameters:
        event_id (str): The ID of the event.

    Returns:
        A JSON response containing the bookings for the event if they exist,
        or a JSON response with a 'No bookings found' message and a 404 status code if no bookings are found.
        If an error occurs during the process, a JSON response with an 'An error occurred' message and a 500 status code is returned.
    """
    try:
        # Validate the event_id
        schema = IdSchema()
        event_id = schema.load({'id': event_id})

        # Query the bookings
        bookings = Booking.query.filter_by(event_id=event_id).all()

        # Check if the bookings exist
        if bookings is None:
            return jsonify({'message': 'No bookings found'}), 404

        # Format the bookings
        formatted_bookings = [booking.format() for booking in bookings]

        # Return the bookings
        return jsonify({'message': 'Bookings found', 'data': formatted_bookings}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500