## Endpoint Routes for User Blueprint
from flask import Blueprint, request, jsonify
from bookingapp.models.user import User
from bookingapp import db
#from bookingapp.utils.uuid_validation import IdSchema
from uuid import UUID
from werkzeug.security import generate_password_hash


# Create the User blueprint
user_bp = Blueprint('user', __name__, url_prefix='/api/v1/user')

# Route to get all users for testing
@user_bp.route('/all', methods=['GET'])
def get_all_users():
    try:
        # Query all users from the database
        users = User.query.all()

        # Format the users
        formatted_users = [user.format() for user in users]

        # Return the formatted users
        return jsonify({'message': 'Users retrieved successfully', 'data': formatted_users}), 200

    except Exception as e:
        # Return an error response if retrieval fails
        return jsonify({'message': 'Error retrieving users', 'error': str(e)}), 500


# Route to register a new user in order to test my booking routes
@user_bp.route('/register', methods=['POST'])
def register_user():
    try:
        #schema = IdSchema()
        # Get user data from the request
        data = request.get_json()

        # Validate the user data using the schema
        #user_id = schema.load(data)

        # Check if the user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 400

        # Hash the user's password
        hashed_password = generate_password_hash(data['password'])

        # Create a new user instance
        new_user = User(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password_hash=hashed_password,
            avatar=data['avatar'],
            is_verified=data['is_verified'],
            is_admin=data['is_admin'],
            is_active=data['is_active']
            # Add other user attributes as needed
        )

        # Insert the new user into the database
        new_user.insert()

        # Return a success response
        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        # Return an error response if registration fails
        return jsonify({'message': 'User registration failed', 'error': str(e)}), 500