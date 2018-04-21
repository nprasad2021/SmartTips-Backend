from . import api
from flask import jsonify, abort, request
import geopy
from app.models import Place

from api.authentication import requires_authentication


@api.route('/places/')
def places_for_location():
    latitude = request.args['latitude']
    longitude = request.args['longitude']
    if latitude is None and longitude is None:
        return jsonify({ 'message': 'Invalid url parameters' }), 400

    required_distance = 20 # km
    user_location = geopy.Point(latitude, longitude)
    all_places = Place.query.all()
    result = []
    for place in all_places:
        if geopy.distance.distance(place.location(), user_location).km < required_distance:
            result.append(place)


    return jsonify(places=result), 200
