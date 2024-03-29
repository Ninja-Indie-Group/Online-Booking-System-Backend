from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from bookingapp import db
from bookingapp.models.user import User
from functools import wraps
from datetime import datetime, timedelta
from random import randint
from bookingapp.auth.auth_utils import login_required, admin_required, send_otp_email, validate_email, validate_password
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, decode_token, get_jwt_identity, get_jwt, unset_jwt_cookies

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


# Endpoint for user registration
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    mandatory_fields = ['email', 'password', 'first_name', 'last_name']

    missing_fields = [field for field in mandatory_fields if field not in data]

    if missing_fields:
        return jsonify({'message': f'{missing_fields} is required'}), 400

    # turn email to lowercase
    data['email'] = data['email'].lower()

    # Use Regex to Check if the email is valid
    if not validate_email(data['email']):
        return jsonify({'message': 'Invalid email'}), 400


    try:
        # Check if the username is already taken
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'message': 'Email already exists'}), 400

        validation_result = validate_password(data['password'])
        if validation_result is not None:
                return jsonify({'message': validation_result}), 400


        # Create a new user
        new_user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'], password=generate_password_hash(data['password']))
        new_user.insert()

        # Generate and store the OTP with its expiry time
        otp = str(randint(1000, 9999))  # Generate a 4-digit OTP
        otp_expiry = datetime.now() + timedelta(minutes=10)  # Set expiry time to 10 minutes from now
        new_user.otp = otp
        new_user.otp_expiry = otp_expiry
        new_user.insert()

        # Send the OTP to the user's email (implement send_otp_email function)
        full_name = new_user.first_name + " " + new_user.last_name
        send_otp_email(full_name, new_user.email, otp)

        access_token = create_access_token(identity=new_user.id, expires_delta=timedelta(hours=1))   # Access token expires in 1 hour
        refresh_token = create_refresh_token(identity=new_user.id, expires_delta=timedelta(days=90))  # Refresh token expires in 24 hours

        # get user data
        userData = {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "createdAt": new_user.createdAt,
        }
        return jsonify({'message': 'User registered. OTP sent to email for verification.', 'userData': userData}), 201
    except Exception as e:
        db.session.rollback()
        current_app.log_exception(exc_info=e)
        return (
            jsonify(
                {
                    "error": "Internal server error",
                    "message": "It's not you it's us",
                    "status": False,
                }
            ),
            500,
        )
    #--------Logic to Send Email for confirmation --------

#     # Generate and return an authentication token for the new user
#     token = generate_token(new_user.id)  # Token expiration time: 10 minutes

#     # Send an email with the tokenized link
#     full_name = new_user.first_name + " " + new_user.last_name
#     send_register_email(full_name, new_user.email, token)

 #   return jsonify({'message': 'User registered. Confirmation email sent.'}), 201

# Endpoint to confirm the OTP sent to the email
@auth_bp.route('/confirm_otp', methods=['POST'])
def confirm_otp():
    data = request.json

    if 'email' not in data or 'otp' not in data:
        return jsonify({'message': 'Incomplete data'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    otp = str(data['otp'])

    if not user.otp or user.otp != otp:
        return jsonify({'message': 'Invalid OTP'}), 400

    if datetime.now() > user.otp_expiry:
        return jsonify({'message': 'OTP expired'}), 400

    # OTP matches and is within the expiry time, confirm the email
    user.is_verified = True
    user.update()
    return jsonify({'message': 'Email confirmed successfully'}), 200

# Endpoint to resend OTP to the user's email
@auth_bp.route('/resend_otp', methods=['POST'])
def resend_otp():
    data = request.json
    if 'email' not in data:
        return jsonify({'message': 'Email is required to resend OTP'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.email_confirmed:
        return jsonify({'message': 'Email already confirmed'}), 400

    # Generate a new OTP
    new_otp = str(randint(1000, 9999))  # Generate a new 6-digit OTP

    # Update the user's OTP in the database
    user.otp = new_otp
    otp_expiry = datetime.now() + timedelta(minutes=10)  # Set expiry time to 10 minutes from now
    user.otp_expiry = otp_expiry
    user.update()

    # Resend the OTP to the user's email (implement send_otp_email function)
    # Send the OTP to the user's email (implement send_otp_email function)
    full_name = user.first_name + " " + user.last_name
    send_otp_email(full_name, user.email, new_otp)

    return jsonify({'message': 'New OTP sent to email'}), 200

# # Endpoint to confirm the email
# @auth_bp.route('/confirm_email/<token>', methods=['GET'])
# def confirm_email(token):
#     s = Serializer(current_app.config['SECRET_KEY'])
#     try:
#         data = s.loads(token)
#         user = User.query.get(data['user_id'])
#         if not user or user.email_confirmation_token_used:
#             raise Exception()
#     except Exception as e:
#         return jsonify({'message': 'Invalid or expired token'}), 400

#     # Mark the token as used
#     user.email_confirmation_token_used = True

#     # Mark the user's email as confirmed
#     user.email_confirmed = True
#     db.session.commit()

#     return jsonify({'message': 'Email confirmed successfully'}), 200

# Endpoint for user login and token generation
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    # Check if required fields are present in the request data
    if 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    # turn email to lowercase
    data['email'] = data['email'].lower()

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Generate and return an authentication token for the user
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))   # Access token expires in 1 hour
    refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(days=90))  # Refresh token expires in 24 hours

    # get user data
    userData = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile_picture": user.avatar,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "createdAt": user.createdAt,
        "updatedAt": user.updatedAt
        }
    return jsonify({'userData': userData, 'message': 'Logged in successfully'}), 200

# Endpoint for token refresh
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id, expires_delta=timedelta(hours=1))
    return jsonify(access_token=new_access_token, message='Token refreshed successfully'), 200


# Endpoint for user logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


# Endpoint for user profile
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user = get_jwt_identity()
    print(user)
    user = User.query.get(user)
    return jsonify(user.format())

# Endpoint for user profile update
@auth_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile(user):
    data = request.json
    if 'email' in data:
        user.email = data['email']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify(user.format()), 200

# Endpoint for user profile deletion
@auth_bp.route('/profile', methods=['DELETE'])
@admin_required
def delete_profile(user):
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Profile deleted successfully'}), 200

# Endpoint to get all users
@auth_bp.route('/users', methods=['GET'])
@admin_required
def get_users(user):
    users = User.query.all()
    total = len(users)
    return jsonify([user.format() for user in users], "total_users:", total), 200

# Endpoint to get a user by ID
@auth_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.format()), 200

# Endpoint to update a user by ID
@auth_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.json
    if 'email' in data:
        user.email = data['email']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'username' in data:
        user.username = data['username']
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify(user.format()), 200

# Endpoint to delete a user by ID
@auth_bp.route('/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


# Endpoint to make a user an admin
@auth_bp.route('/users/<user_id>/admin', methods=['PATCH'])
@login_required
def make_admin(user, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.is_admin = True
    db.session.commit()
    return jsonify(user.format()), 200

# Endpoint to remove admin privileges from a user
@auth_bp.route('/users/<user_id>/admin', methods=['DELETE'])
@login_required
def remove_admin(user, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.is_admin = False
    db.session.commit()
    return jsonify(user.format()), 200

# Endpoint to deactivate a user
@auth_bp.route('/users/<user_id>/deactivate', methods=['PATCH'])
@login_required
def deactivate_user(user, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.is_active = False
    db.session.commit()
    return jsonify(user.format()), 200

# Endpoint to activate a user
@auth_bp.route('/users/<user_id>/activate', methods=['PATCH'])
@login_required
def activate_user(user, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.is_active = True
    db.session.commit()
    return jsonify(user.format()), 200

# Endpoint to get all admins
@auth_bp.route('/admins', methods=['GET'])
@admin_required
def get_admins(user):
    admins = User.query.filter_by(is_admin=True).all()
    total = len(admins)
    return jsonify([admin.format() for admin in admins], "total_admins:", total), 200

# Endpoint to get all active users
@auth_bp.route('/users/active', methods=['GET'])
@admin_required
def get_active_users(user):
    active_users = User.query.filter_by(is_active=True).all()
    total = len(active_users)
    return jsonify([user.format() for user in active_users], "total_active_users:", total), 200

# Endpoint to get all inactive users
@auth_bp.route('/users/inactive', methods=['GET'])
@admin_required
def get_inactive_users(user):
    inactive_users = User.query.filter_by(is_active=False).all()
    total = len(inactive_users)
    return jsonify([user.format() for user in inactive_users], "total_inactive_users:", total), 200

# Endpoint to get all verified users
@auth_bp.route('/users/verified', methods=['GET'])
@admin_required
def get_verified_users(user):
    verified_users = User.query.filter_by(email_confirmed=True).all()
    total = len(verified_users)
    return jsonify([user.format() for user in verified_users], "total_verified_users:", total), 200

# Endpoint to get all unverified users
@auth_bp.route('/users/unverified', methods=['GET'])
@admin_required
def get_unverified_users(user):
    unverified_users = User.query.filter_by(is_verified=False).all()
    total = len(unverified_users)
    return jsonify([user.format() for user in unverified_users], "total_unverified_users:", total), 200

# Route to test the server
@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Server is up and running'}), 200
