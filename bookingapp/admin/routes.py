## Endpoint Routes for Admin Blueprint
from flask import Blueprint, request, jsonify
from bookingapp.models.admin import Admin
from bookingapp import db
from bookingapp.utils.uuid_validation import IdSchema
from uuid import UUID

# Create the admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

# test
@admin_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Admin Blueprint Working'}), 200