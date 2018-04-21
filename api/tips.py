from . import api
from flask import jsonify, abort, request
from app.models import Tip, User
from app import db

from api.authentication import requires_authentication


@api.route('/tips/', methods=['POST'])
@requires_authentication
def create_tip(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify(message='user not found'), 400

    try:
        place_id = request.json['place_id']
        amount = request.json['amount']
        rate = request.json['rate']
    except:
        return jsonify(message='invalid json parameters'), 400

    try:
        comment = request.json['comment']
    except:
        comment = None

    if place_id is None or amount is None or rate is None:
        return jsonify(message='invalid tip parameters'), 400

    tip = Tip(place_id, user_id, amount, rate, comment)
    db.session.add(tip)
    db.session.commit()

    return jsonify(tip=tip.serialize()), 200
