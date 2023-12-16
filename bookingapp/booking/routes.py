## Endpoint Routes for Booking Blueprint
from flask import Blueprint, request, jsonify
from bookingapp.models.booking import Booking
from bookingapp import db
from bookingapp.utils.uuid_validation import validate_uuid, ValidationError

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
        or a JSON response with a 'No bookings found' message and a 404 status
        code if no bookings are found. If an error occurs during the process,
        a JSON response with an 'An error occurred' message and a 500 status
        code is returned.
    """
    try:
        # Validate the event_id
        event_id = validate_uuid(event_id)

        # Query the bookings
        bookings = Booking.query.filter_by(event_id=event_id).all()

        # Check if the bookings exist
        if not bookings:
            return jsonify({'message': 'No bookings found'}), 404

        # Format the bookings
        formatted_bookings = [booking.format() for booking in bookings]

        # Return the bookings
        return jsonify({'message': 'Bookings found', 'data': formatted_bookings}), 200
    except ValidationError as ve:
        return jsonify({'message': 'Validation error', 'error': ve.errors()}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

# Route to get bookings for a user
@booking_bp.route('/user/<user_id>', methods=['GET'])
def get_bookings_for_user(user_id):
    try:
        # Validate the user_id
        user_id = validate_uuid(user_id)

        # Query the bookings for the user
        bookings = Booking.query.filter_by(user_id=user_id).all()

        # Check if the bookings exist
        if not bookings:
            return jsonify({'message': 'No bookings found for the user'}), 404

        # Format the bookings
        formatted_bookings = [booking.format() for booking in bookings]

        # Return the bookings
        return jsonify({'message': 'Bookings found for the user', 'data': formatted_bookings}), 200

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
        or a JSON response with an 'An error occurred' message and a 500
        status code if an error occurs during the process.
    """
    try:
        # Validate the event_id
        event_id = validate_uuid(event_id)

        # Extract user_id and other necessary data from the request
        user_id = request.json.get('user_id')

        # Check if a booking already exists for the user and event
        existing_booking = Booking.query.filter_by(user_id=user_id, event_id=event_id).first()
        if existing_booking:
            return jsonify({'message': 'User already has a booking for this event'}), 400

        # Create a new booking instance and add it to the database
        booking = Booking(user_id=str(user_id), event_id=str(event_id))
        booking.insert()

        # Return the created booking
        formatted_booking = booking.format()
        return jsonify({'message': 'Booking has been successful', 'data': formatted_booking}), 201
    except ValidationError as ve:
        return jsonify({'message': 'Validation error', 'error': ve.errors()}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
    
    
@booking_bp.route('/<booking_id>', methods=['PUT'])
def update_booking(booking_id):
    """
    Updates an existing booking.

    Parameters:
        booking_id (str): The ID of the booking.

    Returns:
        A JSON response containing the updated booking if successful,
        or a JSON response with an 'An error occurred' message and a 500 status
        code if an error occurs during the process.
    """
    try:
        # Validate the booking_id
        booking_id = validate_uuid(booking_id)

        # Retrieve the booking from the database
        booking = Booking.query.get(booking_id)

        # Check if the booking exists
        if not booking:
            return jsonify({'message': 'Booking not found'}), 404

        # Update the booking attributes based on the request data
        # For example: booking.attribute = request.json.get('new_value')
        # Then, commit the changes to the database
        # booking.update()

        # Return the updated booking
        # formatted_booking = booking.format()
        # return jsonify({'message': 'Booking updated', 'data': formatted_booking}), 200

        # For now, return a placeholder response
        return jsonify({'message': 'Update booking route placeholder'}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

# Route to delete a an existed Booking
@booking_bp.route('/<booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    """
    Deletes an existing booking.

    Parameters:
        booking_id (str): The ID of the booking.

    Returns:
        A JSON response with a 'Booking deleted' message if successful,
        or a JSON response with an 'An error occurred' message and a 500 status code
        if an error occurs during the process.
    """
    try:
        # Validate the booking_id
        booking_id = validate_uuid(booking_id)

        # Retrieve the booking from the database
        booking = Booking.query.get(booking_id)

        # Check if the booking exists
        if not booking:
            return jsonify({'message': 'Booking not found'}), 404

        # Delete the booking from the database
        booking.delete()

        # Return a response indicating successful deletion
        return jsonify({'message': 'Booking deleted'}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500