# -*- coding: utf-8 -*-
import httplib2
import json


with open('config.json') as json_data_file:
    data = json.load(json_data_file)
    global google_api_key
    google_api_key = data['google_api_key']


def get_geocode_location(input_string):
    location_string = input_string.replace(" ", "+")

    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (location_string, google_api_key))
    # tekee olion, jolla voi requestin tehdä
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude, longitude)
