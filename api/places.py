from . import api
from flask import jsonify

from api.authentication import requires_authentication

@api.route('/places/')
@requires_authentication
def places_for_location(user_id):
    return jsonify({'user_id': user_id})
