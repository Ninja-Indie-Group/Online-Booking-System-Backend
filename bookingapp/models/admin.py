#!/usr/bin/env python3
"""Admin Entity model"""
from bookingapp.models.base import BaseModel
from bookingapp import db
import bcrypt


class Admin(BaseModel):
    """Admin entity class"""

    __tablename__ = "admins"

    # Define columns for the Admin table
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_superadmin = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=True)


#     # Relationship with Event model
#     event = db.relationship(
#         "Event", backref="admin", cascade="all, delete-orphan", lazy=True
#     )

    def __init__(self, username, email, password, company, position, first_name, last_name, user_id, is_superadmin=False):
        """Initialize the Admin object"""
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        self.company = company
        self.position = position
        self.first_name = first_name
        self.last_name = last_name
        self.is_superadmin = is_superadmin
        self.user_id = user_id

    def __repr__(self):
        """Return a string representation of the Admin object"""
        return (
            f"Id: {self.id}, Username: {self.username}, "
            f"Email: {self.email}"
        )


    def format(self):
        """Format the Admin object's attributes as a dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'company': self.company,
            'position': self.position,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'is_superadmin': self.is_superadmin,
            'user_id': self.user_id
        }

    @property
    def full_name(self):
        """Returns the admin full name"""
        return f"{self.first_name} {self.last_name}"

    @property
    def password(self):
        """Returns the hashed password"""
        return self._password

    @password.setter
    def password(self, password):
        """Sets the hashed password"""
        self._password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        """Verifies if the provided password matches the hashed password"""
        return bcrypt.checkpw(
            password.encode('utf-8'), self._password.encode('utf-8'))

    def format(self):
        """Format the Admin object's attributes as a dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'company': self.company,
            'position': self.position,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
        }

    def __repr__(self):
        """Return a string representation of the Admin object"""
        return (f"Id: {self.id}, Username: {self.username}, Name: {self.full_name}, Email: {self.email}"
        )
