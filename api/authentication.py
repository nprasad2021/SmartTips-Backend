# coding: utf-8

from flask import g, jsonify
from flask import request
from . import api
from app.models import User
from api.errors import unauthorized

def validate_token(access_token):
    user = User.query.filter_by(api_token=access_token).first()
    if user:
        return user.id
    else:
        return None

def requires_authentication(fn):
    def _wrap(*args, **kwargs):
        if 'Authorization' not in request.headers:
            # Unauthorized
            print("No token in header")
            return unauthorized('lol')

        print("Checking token...")
        user_id = validate_token(request.headers['Authorization'])
        if user_id is None:
            print("Check returned FAIL!")
            # Unauthorized
            return unauthorized('lol')

        return fn(user_id=user_id, *args, **kwargs)
    return _wrap
