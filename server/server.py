#! /usr/bin/python

from pymongo import MongoClient
from flask import Flask, json

# globals
URI = "mongodb://comp50-mongo:cgAWFSlExkZp33BpFjuJLmGO7oFe31CigL3wQ0Fte6klnszZpPklc6CUfsBPNN89svY8uBK73Z9yQRWGzP83OA==@comp50-mongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
client = MongoClient(URI)


api = Flask(__name__)
users = [{"name": "Fabrice B. Mpogazi", "email":"fbigabiro@gmail.com"}]

@api.route('/users', methods=['GET'])
def get_users():
	return json.dumps(users)

@api.route('/user_watchlist', methods=['POST'])
def get_user_watchlist():
	pass

@api.route('/update_stock', methods=['POST'])
def post_update_stock():
	pass

@api.route('/create_watchlist', methods=['POST'])
def create_watchlist():
	pass

if __name__ == "__main__":
	api.run()