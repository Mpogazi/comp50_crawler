#! /usr/bin/python

from pymongo import MongoClient
from flask import Flask, json, request
from bson.json_util import dumps

# globals

URI = "mongodb://heroku_z03b9kqp:eit8th40c96ss3e2mqlph3loo5@ds253418.mlab.com:53418/heroku_z03b9kqp"
db_50    = MongoClient(URI)['concurrency']
listings = db_50['listings']
stocks   = db_50['stocks']
users    = db_50['users']
websites = db_50['websites']


api = Flask(__name__)

@api.route('/', methods=['GET'])
def get_index():
	return json.dumps('successfully set the app')

@api.route('/add_user', methods=['POST'])
def add_user():
	req_data = request.get_json()
	return json.dumps(req_date)


@api.route('/users', methods=['GET'])
def get_users():
	return json.dumps(user)

@api.route('/user', methods=['POST'])
def get_user():
	data = request.get_json()
	try:
		username = data['name']
		user = dumps(users.find({"name": username}))
		return user
	except:
		return json.dumps({})

@api.route('/user_watchlist', methods=['POST'])
def get_user_watchlist():
	data = request.get_json()
	try:
		username = data['name']
		user     = dumps(users.find({"name": username}))
		return user['wishlist']
	except:
		return json.dumps({})

@api.route('/update_stock', methods=['POST'])
def post_update_stock():
	data = request.get_json()
	try:
		stock = data['company']
		user  = dumps(users.update())
		return {data: "Successfully updated"}
	except:
		return {data: "Failed to Update"}

@api.route('/create_watchlist', methods=['POST'])
def create_watchlist():
	pass

if __name__ == "__main__":
	api.run(threaded=True, port=5000)