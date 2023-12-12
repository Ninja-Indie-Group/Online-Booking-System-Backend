#!/usr/bin/env python3
"""User Entity Module"""
from bookingapp.models.base import BaseModel
from bookingapp import db


class User(BaseModel):
    """User model"""

    # Use the default behavior for the table name
    __tablename__ = "users"


    # Adjust the length of string columns based on your requirements
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
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
            'attendees', lazy='dynamic')
    )

    def __init__(self, username, name, email, password_hash, avatar, is_verified=False, is_admin=False, is_active=True):
        """Initialize the User object"""
        super().__init__()
        self.username = username
        self.name = name
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
            f"Name: {self.name}, Email: {self.email}"
            )

    # Override the format method to return user attributes as a dictionary
    def format(self):
        """Return a dictionary representation of the User object"""
        return {
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "avatar": self.avatar,
            "is_verified": self.is_verified,
            "is_admin": self.is_admin,
            "is_active": self.is_active,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }