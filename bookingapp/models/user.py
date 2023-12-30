#!/usr/bin/env python3
"""User Entity Module"""
from bookingapp.models.base import BaseModel
from bookingapp import db


class User(BaseModel):
    """User model"""

    # Use the default behavior for the table name
    __tablename__ = "users"

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=False)
    otp = db.Column(db.String(6), nullable=True, default=None)
    otp_created_at = db.Column(db.DateTime, nullable=True, default=None)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)


    def __init__(self, first_name, last_name, email, password, avatar='deault.jpg', is_verified=False, is_admin=False, is_active=True):
        """Initialize the User object"""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.avatar = avatar
        self.is_verified = is_verified
        self.is_admin = is_admin
        self.is_active = is_active




    def __repr__(self):
        """Return a string representation of the User object"""
        return (
            f"Name: {self.name}, Email: {self.email}"
            )

    # Override the format method to return user attributes as a dictionary
    def format(self):
        """Return a dictionary representation of the User object"""
        return {
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