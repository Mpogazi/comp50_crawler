#! /usr/bin/python

from pymongo import MongoClient
# import requests
from flask import Flask, json, request, jsonify
from bson.json_util import dumps
import os
import sendgrid
from sendgrid.helpers.mail import *

URI = "ds253418.mlab.com"
db_50    = MongoClient(URI, 53418)
db_50    = db_50['heroku_z03b9kqp']
db_50.authenticate('concurrency', 'Rwanda@123456')
listings = db_50['listings']
stocks   = db_50['stocks']
users    = db_50['users']
websites = db_50['websites']

api = Flask(__name__)

@api.route('/', methods=['GET'])
def get_index():
	return json.dumps('successfully set the app')

@api.route('/websites', methods=['GET'])
def get_websites():
	result = websites.find({})
	return ({'data': result}, 200)

@api.route('/add_websites', methods=['POST'])
def add_websites():
	req_data = request.json
	webs     = req_data['websites']
	try:
		websites.update({}, {'$addToSet': {'websites': {'$each': webs}}}, upsert=True)
		return ('successfully updated websites', 200)
	except Exception as e:
		return ('Failed Miserably', 404)

@api.route('/get_companies', methods=['GET'])
def get_companies():
	result = []
	for company in listings.find():
		temp = {'name': company['Name'], 'symbol': company['Symbol']}
		result.append(temp)
	return ({ 'data': result }, 200)

@api.route('/get_company_info', methods=['POST'])
def get_company_info():
	req_data = request.get_json()
	name = req_data['name']
	try:
		company = listings.find({'Name': name})
		for cp in company:
			result = {'name': cp['Name'], 'symbol': cp['Symbol']}
		return (result, 200)
	except Exception as e:
		return ('Could not find company', 404)

@api.route('/add_user', methods=['POST'])
def add_user():
	req_data = request.json
	name = req_data['name']
	email = req_data['email']
	watchlist = req_data['watchlist']
	users.insert_one({ 'name': name, 'email': email, 'watchlist': watchlist })
	return ('successfully added user', 200)

@api.route('/add_mention', methods=['POST'])
def add_mention():
	req_data = request.json
	name = req_data['name']
	updates = req_data['update']
	stocks.find_one_and_update({'name': name}, {'$set': {'name': name},'$addToSet': 
										{'mentions': {'$each': updates}}}, upsert=True)
	return ('successfully added mention', 200)

@api.route('/add_watchlist', methods=[''])
def add_watchlist():
	req_data = request.json
	email = req_data['email']
	watchlist = req_data['watchlist']
	try:
		users.update({'email': email}, {'$addToSet': {'watchlist': {'$each': watchlist }}})
		return ('successfully added watchlist', 200)
	except Exception as e:
		return ('Failed miserably', 404)

@api.route('/users', methods=['GET'])
def get_users():
	list_users = users.find({})
	return ({'data' : list_users}, 200)

if __name__ == "__main__":
	api.run()