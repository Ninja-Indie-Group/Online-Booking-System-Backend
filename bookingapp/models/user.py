#!/usr/bin/env python3
"""User Entity Module"""
from bookingapp.models.base import BaseModel
from bookingapp import db
from bookingapp.models import event_attendees


class User(BaseModel):
    """User model"""

    # Use the default behavior for the table name
    __tablename__ = "users"


    # Define column for the user table
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=False)
    otp = db.Column(db.String(6), nullable=True, default=None)
    otp_created_at = db.Column(db.DateTime, nullable=True, default=None)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)


    attended_events = db.relationship(
        'Event', secondary='event_attendees', backref=db.backref(
            'attendees_list', lazy='dynamic')
        )


    def __init__(self, username, first_name, last_name, email, password_hash, avatar, is_verified=False, is_admin=False, is_active=True):
        """Initialize the User object"""
        super().__init__()
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.avatar = avatar
        self.is_verified = is_verified
        self.is_admin = is_admin
        self.is_active = is_active




    def __repr__(self):
        """Return a string representation of the User object"""
        return (
            f"Id: {self.id}, Username: {self.username}, "
            f"Name: {self.first_name} {self.last_name}, Email: {self.email}"
            )

    # Override the format method to return user attributes as a dictionary
    def format(self):
        """Return a dictionary representation of the User object"""
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "avatar": self.avatar,
            "is_verified": self.is_verified,
            "is_admin": self.is_admin,
            "is_active": self.is_active,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }