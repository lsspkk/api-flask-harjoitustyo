# -*- coding: utf-8 -*-
import httplib2
import json
from geocode import *




with open('config.json') as json_data_file:
    data = json.load(json_data_file)
    fs_client_id = data['foursquare_client_id']
    fs_client_secret = data['foursquare_client_secret']

def find_food(meal, location):
    # use get_geocode_location to get the coordinates
    lat, lng = get_geocode_location(location)



    # use foursquare to find a nearby restaurant
    # https://api.foursquare.com/v2/venues/search?v=20170212&ll

    
    url = ('https://api.foursquare.com/v2/venues/search?v=20170212&ll=%s,%s&client_id=%s&client_secret=%s&query=%s' % (lat,lng,fs_client_id,fs_client_secret,meal))
    # tekee olion, jolla voi requestin tehdä
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)

    # get the first
    restaurant = result['response']['venues'][0]
    restaurant_name = restaurant['name']
    restaurant_address = restaurant['location']['formattedAddress']
    restaurant_info =  { 'name': restaurant_name, 'address': restaurant_address }

    return restaurant_info


#print find_food('pizza', "tampere")
#print find_food('sushi', "suomi")
