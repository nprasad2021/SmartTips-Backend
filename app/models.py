# coding: utf-8

from flask import current_app
from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    facebook_access_token = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location_latitude = db.Column(db.Numeric, nullable=False)
    location_longitude = db.Column(db.Numeric, nullable=False)
    tips = db.relationship('Tip', backref='place', lazy=True)
    waiters = db.relationship('Waiter', backref='place', lazy=True)

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

