#!/usr/bin/env python3
"""Booking Entity model"""
from bookingapp.models.base import BaseModel
from bookingapp import db
from bookingapp.models.user import User
from bookingapp.models.event import Event
from datetime import datetime

class Booking(BaseModel):
    '''Booking model class'''
    __tablename__ = 'bookings'

    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.String(255), db.ForeignKey('events.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    event = db.relationship('Event', backref=db.backref('bookings', lazy=True))

    def __init__(self, user_id, event_id, booking_date):
        """Initialize the Booking object"""
        super().__init__()
        self.user_id = user_id
        self.event_id = event_id
        self.booking_date = booking_date

    def __repr__(self):
        """Return a string representation of the Booking object"""
        return f"Booking ID: {self.id}, User: {self.user.username}, Event: {self.event.event_name}, Booking Date: {self.booking_date}"

    def format(self):
        """Return a dictionary representation of the Booking object"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_id": self.event_id,
            "booking_date": self.booking_date
        }
