# coding: utf-8

from flask import jsonify

def bad_request(msg):
    r = jsonify({'error': 'bad request', 'message': msg})
    r.status_code = 400
    return r

def unauthorized(msg):
    r = jsonify({'error': 'unauthorized', 'message': msg})
    r.status_code = 401
    return r
