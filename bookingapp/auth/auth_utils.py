from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify, url_for, render_template
from functools import wraps
from bookingapp.models.user import User
from flask_mail import Message
from bookingapp import mail
import re



# Decorator to check if the user is logged in
def login_required(f):
    """
    Decorator function to enforce login requirement for a given function.

    Parameters:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Raises:
        Exception: If the authorization header is missing or the token is invalid.

    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if not user or not user.is_active:
                return jsonify({'Unauthorized access'}), 401
        except Exception as e:
            return jsonify({'Invalid token'}), 401

        return f(user, *args, **kwargs)

    return decorated_function

# Decorator to check if the user is an admin
def admin_required(f):
    """
    Decorator function to enforce login requirement for a given function.

    Parameters:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Raises:
        Exception: If the authorization header is missing or the token is invalid.

    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if not user or not user.is_active or not user.is_admin:
                return jsonify({'Unauthorized access'}), 401
        except Exception as e:
            return jsonify({'Invalid token'}), 401

        return f(user, *args, **kwargs)

    return decorated_function



def send_otp_email(name, email, otp):
    # Send an email with the OTP
    try:
        # Create the message for the user
        msg_title = "Registration Confirmation - Booking App"
        sender = "noreply@app.com"
        msg = Message(msg_title, sender=sender, recipients=[email])
        msg_body = "Please use this verification code to confirm your registration"
        msg.body = ""
        msg.reply_to = "bookingapp@gmail.com"
        data = {
            'app_name': "Booking App",
            'title': msg_title,
            'body': msg_body,
            'name': name,
            'otp': otp
        }
        msg.html = render_template("email_otp.html", data=data)

        # Send the message
        mail.send(msg)

    except Exception as e:
        return {'msg': 'Email not sent', 'error': str(e)}, 500




def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    if len(password) < 6:
        return 'Password must be at least 6 characters'
    if not re.search("[a-z]", password):
        return 'Password must contain at least one lowercase letter'
    if not re.search("[A-Z]", password):
        return 'Password must contain at least one uppercase letter'
    if not re.search("[0-9]", password):
        return 'Password must contain at least one number'
    if re.search("\s", password):
        return 'Password cannot contain spaces'
    if re.search("[\"\']", password):
        return 'Password cannot contain quotes'
    if password == "password":
        return 'Password too common'
    if password == "123456":
        return 'Password too common'
    if password == "123456789":
        return 'Password too common'
    if password == "qwerty":
        return 'Password too common'
    if password == "password123":
        return 'Password too common'
    if password == "abc123":
        return 'Password too common'
    if password == "abcedf":
        return 'Password too common'
    return None