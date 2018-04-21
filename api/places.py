from . import api
from flask import jsonify, abort, request
import geopy
from geopy import distance
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
        place_location = place.location()
        distance_to_place = distance.distance(place_location, user_location).km
        if distance_to_place < required_distance:
            result.append(place.serialize())


    return jsonify(places=result), 200
