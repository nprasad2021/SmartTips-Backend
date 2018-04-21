# coding: utf-8

from flask import current_app
from . import db
from datetime import datetime
import secrets
from geopy import Point

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    api_token = db.Column(db.String, unique=True, nullable=False, default=secrets.token_urlsafe)

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=True)
    location_latitude = db.Column(db.Numeric, nullable=False)
    location_longitude = db.Column(db.Numeric, nullable=False)
    is_tipping_available = db.Column(db.Boolean, nullable=False, default=True)
    is_place_tippting_available = db.Column(db.Boolean, nullable=False, default=True)
    tips = db.relationship('Tip', backref='place', lazy=True)
    waiters = db.relationship('Waiter', backref='place', lazy=True)

    def __init__(self, name, address, location_latitude, location_longitude, is_tipping_available):
        self.name = name
        self.address = address
        self.location_latitude = location_latitude
        self.location_longitude = location_longitude
        self.is_tipping_available = is_tipping_available

    def location(self):
        return Point(self.location_latitude, self.location_longitude)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'location_latitude': self.location_latitude,
            'location_longitude': self.location_longitude,
            'is_tipping_available': self.is_tipping_available,
            'is_place_tippting_available': self.is_place_tippting_available,
            'tips': [tip.serialize() for tip in self.tips]
        }

class Waiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    login = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    tips = db.relationship('Tip', backref='waiter', lazy=True)

class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric, nullable=False, default=0)
    comment = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    waiter_id = db.Column(db.Integer, db.ForeignKey('waiter.id'), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'comment': self.comment,
            'created_at': self.created_at.isoformat()
        }
