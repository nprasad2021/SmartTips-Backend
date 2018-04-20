from flask import Blueprint, g, jsonify

api = Blueprint('api', __name__)

from .errors import unauthorized

@api.route('/me/')
def tell_me_about_me():
    u = g.current_user
    if u.is_anonymous():
        return unauthorized('No info for anonymous user')
    return jsonify({'email': u.email})
