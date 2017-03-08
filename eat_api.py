# -*- coding: utf-8 -*-
#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask, jsonify, abort, json, make_response, url_for
import httplib2
import re
app = Flask(__name__)

from geocode import get_geocode_location
from findfood import *
from simple_authentication import *

locations = [
			{
				'id' : 1,
				'address': u'Hakkarinkatu+2,Tampere',
				'meal': u'pizza'
			},
			{
				'id' : 2,
				'address': u'Kuntokatu+3,Tampere',
				'meal': u'coffee'
			},
			{
				'id' : 3,
				'address' : u'Santalahdentie,tampere',
				'meal' : u'sushi'
			}
		]

#GET REQUEST
@app.route('/eat', methods=['GET'])
def get_todo():
	abort(401)


#GET REQUEST
@app.route('/eat/locations', methods=['GET'])
@requires_auth
def get_tasks():
	resp = jsonify({'locations': locations})
	resp.status_code = 200
	return resp

@app.route('/eat/location/<int:location_id>', methods=['GET'])
@requires_auth
def get_location(location_id):
	# item on välimuuttuja, joka tarvitaan, jotta task-muuttujaan kopioituu
	task = [ item for item in locations if item['id'] == location_id ]
	if len(task) == 0:
		abort(404)
	# return task[0]['address']
	lat, lng = get_geocode_location(task[0]['address'])
	return jsonify({"lat":lat, "lng":lng})

@app.route('/eat/<int:location_id>', methods=['GET'])
@requires_auth
def eat(location_id):
	task = [ item for item in locations if item['id'] == location_id ]
	if len(task) == 0:
		abort(404)
	food = find_food(task[0]['meal'], task[0]['address'])
	return jsonify({"closest_food":food,
					"related_locations": related_locations(task[0])})

# same city
def related_locations(it):
	city = it['address'].rpartition(',')[-1]
	# print city
	loc =  [ url_for("eat", location_id=item['id']) for item in locations if it['id'] != item['id'] and re.search(re.escape(city), item['address'], re.IGNORECASE) ]
	return loc


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.debug = True
app.run(host='0.0.0.0', port=5000)
