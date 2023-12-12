## Endpoint Routes for User Blueprint
from flask import Blueprint, request, jsonify
from bookingapp.models.user import User
from bookingapp import db
from bookingapp.utils.uuid_validation import IdSchema
from uuid import UUID

# Create the User blueprint
user_bp = Blueprint('user', __name__, url_prefix='/api/v1/user')

# test
@user_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'User Blueprint Working'}), 200