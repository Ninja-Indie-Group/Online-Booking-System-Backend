#!/usr/bin/env python3
"""Attended Events model"""
from bookingapp import db


event_attendees = db.Table(
    'event_attendees',
    db.Column('user_id', db.String(255), db.ForeignKey('users.id'), primary_key=True),
    db.Column('event_id', db.String(255), db.ForeignKey('events.id'), primary_key=True)
)

