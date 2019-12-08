#! /usr/bin/python

from pymongo import MongoClient
from flask import Flask, json, request
from bson.json_util import dumps

# globals
URI = "mongodb://comp50-mongo:cgAWFSlExkZp33BpFjuJLmGO7oFe31CigL3wQ0Fte6klnszZpPklc6CUfsBPNN89svY8uBK73Z9yQRWGzP83OA==@comp50-mongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
db_50    = MongoClient(URI)['concurrency']
listings = db_50['listings']
stocks   = db_50['stocks']
users    = db_50['users']
websites = db_50['websites']
user = ['farmer', 'john', 'tomato']

api = Flask(__name__)

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
	api.run()