## Endpoint Routes for Event Blueprint
from flask import Blueprint, request, jsonify
from bookingapp.models.event import Event
from bookingapp import db
from datetime import datetime
#from bookingapp.utils.uuid_validation import IdSchema
from uuid import UUID

# Create the event blueprint
event_bp = Blueprint('event', __name__, url_prefix='/api/v1/event')

# Route to Create a new Event to test my booking route
@event_bp.route('/', methods=['POST'])
def create_event():
    """
    Creates a new event.

    Returns:
        A JSON response containing the created event if successful,
        or a JSON response with an 'An error occurred' message and a 500 status code if an error occurs during the process.
    """
    try:
        # Extract event data from the request
        event_data = request.json

        # Commented out the admin_id check for testing purposes
        # admin_id = event_data.get('admin_id')  # Adjust based on your data model
        # Ensure that the admin with the given admin_id exists
        # admin = Admin.query.get(admin_id)
        # if not admin:
        #     return jsonify({'message': 'Admin not found'}), 404

        # Create a new event instance and add it to the database
        event = Event(
            event_name=event_data.get('event_name'),
            location=event_data.get('location'),
            date_time=datetime.strptime(event_data.get('date_time'), '%Y-%m-%d %H:%M:%S'),
            description=event_data.get('description'),
            price=event_data.get('price'),
            admin_id=event_data.get('admin_id')  # Uncomment if admin_id is provided in the request
        )
        event.insert()

        # Return the created event
        formatted_event = event.format()
        return jsonify({'message': 'Event created', 'data': formatted_event}), 201
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500