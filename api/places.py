from . import api
from flask import jsonify, abort, request
import geopy
from geopy import distance
from app.models import Place
from functools import reduce
import requests
import json

from api.authentication import requires_authentication

HERE_DISCOVER_BASE_URL = 'https://places.cit.api.here.com/places/v1/discover/here'
DEFAULT_HERE_API_PARAMS = {
    'app_id': 'JTYUMRBXmhKeUTzabYIc',
    'app_code': 'kQsQLTXuAqyS7aOfshiF7Q',
    'cat': 'eat-drink'
}

@api.route('/places/')
def places_for_location():
    latitude = request.args['latitude']
    longitude = request.args['longitude']
    if latitude is None and longitude is None:
        return jsonify({ 'message': 'Invalid url parameters' }), 400

    required_distance = 20 # km
    user_location = geopy.Point(latitude, longitude)
    all_places = Place.query.all()
    close_places = []
    for place in all_places:
        place_location = place.location()
        distance_to_place = distance.distance(place_location, user_location).km
        if distance_to_place < required_distance:
            close_places.append(place)

    additional_places = create_additional_places_request(user_location)
    close_places.extend(additional_places)

    serialized_places = []
    for place in close_places:
        place_data = place.serialize()
        place_data['here_directions_url'] = place.here_directions_url(user_location)
        serialized_places.append(place_data)

    return jsonify(places=serialized_places), 200

def create_additional_places_request(user_location):
    params = DEFAULT_HERE_API_PARAMS
    params['at'] = '{},{}'.format(user_location.latitude,
                                    user_location.longitude)

    try:
        here_api_request = requests.get(HERE_DISCOVER_BASE_URL, params=params)
        response = json.loads(here_api_request.text)
        return convert_here_places_to_native_places(response['results']['items'])
    except:
        return []

def convert_here_places_to_native_places(here_places):
    places = []
    for here_place in here_places:
        place = Place.create_from_here_place(here_place)
        if place is None:
            continue
        places.append(place)

    return places

@api.route('/places/<place_id>/rates/', methods=['GET'])
def get_place_rates(place_id):
    place = Place.query.get(place_id)
    if place is None:
        return jsonify(message='place not found'), 400

    rates = [tip.rate for tip in place.tips]
    average_rate = reduce(lambda x, y: x + y, rates) / len(rates)

    return jsonify(average_rate=int(average_rate), place=place.serialize()), 200
