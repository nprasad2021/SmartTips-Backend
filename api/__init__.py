from flask import Blueprint, g, jsonify

api = Blueprint('api', __name__)

from .errors import unauthorized

@api.route('/test/')
def test_method():
    return jsonify({'message': 'hello world'})

from .places import *
from api.tips import *
