#!/usr/bin/env python3
"""Event Entity Module"""
from bookingapp.models.base import BaseModel
from bookingapp import db
from bookingapp.models.user import User
from datetime import datetime


class Event(BaseModel):
    '''Event model class'''
    __tablename__ = "events"

    event_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    creator = db.relationship('User', backref=db.backref('created_events', lazy=True))

#     attendees = db.relationship(
#         'User', secondary='event_attendees', backref=db.backref(
#             'attended_events', lazy='dynamic'))

    def __init__(self, event_name, location, date_time, description, admin_id):
        """Initialize the Event object"""
        super().__init__()
        self.event_name = event_name
        self.location = location
        self.date_time = date_time
        self.description = description
        self.admin_id = admin_id

    def format(self):
        """Return a dictionary representation of the Event object"""
        return {
            "id": self.id,
            "event_name": self.event_name,
            "location": self.location,
            "date_time": self.date_time,
            "description": self.description,
            "admin_id": self.admin_id
        }

    @classmethod
    def get_events_by_user_id(cls, user_id):
        """Retrieve events associated with a specific user"""
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_upcoming_events(cls):
        """Retrieve upcoming events"""
        return cls.query.filter(
            db.and_(cls.date >= datetime.today()
                    .date(), cls.time >= datetime.now().time())).all()

    @classmethod
    def get_event_details(cls, event_id):
        """Retrieve details of a specific event"""
        return cls.query.get(event_id)

    @classmethod
    def attend_event(cls, user_id, event_id):
        """Mark a user as attending a specific event"""
        event = cls.query.get(event_id)
        if event:
            user = User.query.get(user_id)
            if user:
                event.attendees.append(user)
                db.session.commit()
