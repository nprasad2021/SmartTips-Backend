# coding: utf-8

from flask import current_app
from . import db
from datetime import datetime
import secrets
from geopy import Point
from functools import reduce

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    image_url = db.Column(db.String, unique=False, nullable=False)
    api_token = db.Column(db.String, unique=True, nullable=False, default=secrets.token_urlsafe)
    tips = db.relationship('Tip', backref='user', lazy=True)

    def __init__(self, first_name, last_name, image_url):
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'image_url': self.image_url
        }

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    here_id = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=True)
    rating = db.Column(db.Integer, nullable=True, default=0)
    image_url = db.Column(db.String, nullable=True)
    location_latitude = db.Column(db.Numeric, nullable=False)
    location_longitude = db.Column(db.Numeric, nullable=False)
    is_tipping_available = db.Column(db.Boolean, nullable=False, default=True)
    is_place_tippting_available = db.Column(db.Boolean, nullable=False, default=True)
    tips = db.relationship('Tip', backref='place', lazy=True)
    waiters = db.relationship('Waiter', backref='place', lazy=True)

    def __init__(self, name, address, location_latitude, location_longitude, rating, is_tipping_available):
        self.name = name
        self.address = address
        self.location_latitude = location_latitude
        self.location_longitude = location_longitude
        self.is_tipping_available = is_tipping_available
        self.rating = rating

    def location(self):
        return Point(self.location_latitude, self.location_longitude)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'rating': self.rating,
            'image_url': self.image_url,
            'location_latitude': self.location_latitude,
            'location_longitude': self.location_longitude,
            'is_tipping_available': self.is_tipping_available,
            'is_place_tippting_available': self.is_place_tippting_available,
            'tips': [tip.serialize() for tip in self.tips]
        }

    def here_directions_url(self, user_location):
        return 'here-route://{},{}/{},{}'.format(
            user_location.latitude,
            user_location.longitude,
            self.location_latitude,
            self.location_longitude
        )

    @staticmethod
    def create_from_here_place(here_place):
        try:
            location_latitude = here_place['position'][0]
            location_longitude = here_place['position'][1]
            name = here_place['title']
            address = here_place['vicinity'].split('<')[0]
            rating = here_place['averageRating']
            image_url = here_place['icon']

            place = Place(name, address, location_latitude, location_longitude, rating, False)

            place.image_url = image_url
            place.is_place_tippting_available = False

            return place
        except:
            return None

class Waiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    image_url = db.Column(db.String, unique=False, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    tips = db.relationship('Tip', backref='waiter', lazy=True)

    def __init__(self, first_name, last_name, image_url, place_id):
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url
        self.place_id = place_id

    def balance(self):
        tips_amounts = [tip.amount for tip in Place.query.get(self.place_id).tips]
        if len(tips_amounts) == 0:
            return 0
        return reduce(lambda x, y: x + y, tips_amounts)


    def serialize(self):
        return {
            'place': Place.query.get(self.place_id).serialize(),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'image_url': self.last_name,
            'balance': self.balance()
        }

class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric, nullable=False, default=0)
    rate = db.Column(db.Integer, nullable=False, default=0)
    comment = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    waiter_id = db.Column(db.Integer, db.ForeignKey('waiter.id'), nullable=True)

    def __init__(self, place_id, user_id, amount, rate, comment=None):
        self.amount = amount
        self.rate = rate
        self.comment = comment
        self.user_id = user_id
        self.place_id = place_id

    def serialize(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'comment': self.comment,
            'created_at': self.created_at.isoformat(),
            'user': User.query.get(self.user_id).serialize()
        }
