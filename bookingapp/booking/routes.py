## Endpoint Routes for Booking Blueprint
from flask import Blueprint, request, jsonify
from bookingapp.models.booking import Booking
from bookingapp import db
from bookingapp.utils.uuid_validation import IdSchema
from uuid import UUID

# Create the booking blueprint
booking_bp = Blueprint('booking', __name__, url_prefix='/api/v1/booking')

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
        if not bookings:
            return jsonify({'message': 'No bookings found'}), 404

        # Format the bookings
        formatted_bookings = [booking.format() for booking in bookings]

        # Return the bookings
        return jsonify({'message': 'Bookings found', 'data': formatted_bookings}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

# Route to Create a new Booking
@booking_bp.route('/<event_id>', methods=['POST'])
def create_booking(event_id):
    """
    Creates a new booking for a specific event.

    Parameters:
        event_id (str): The ID of the event.

    Returns:
        A JSON response containing the created booking if successful,
        or a JSON response with an 'An error occurred' message and a 500 status code if an error occurs during the process.
    """
    try:
        # Validate the event_id
        schema = IdSchema()
        event_id = schema.load({'id': event_id})

        # Extract user_id and other necessary data from the request
        user_id = request.json.get('user_id')

        # Create a new booking instance and add it to the database
        booking = Booking(user_id=user_id, event_id=event_id)
        booking.insert()

        # Return the created booking
        formatted_booking = booking.format()
        return jsonify({'message': 'Booking has been successful', 'data': formatted_booking}), 201
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500