from . import api
from flask import jsonify, abort, request
from app.models import Waiter
from app import db

from api.authentication import requires_authentication

@api.route('/waiters/<waiter_id>/', methods=['GET'])
def get_waiter(waiter_id):
    waiter = Waiter.query.get(waiter_id)
    if waiter is None:
        return jsonify(message='waiter not found'), 400

    return jsonify(waiter.serialize()), 200
