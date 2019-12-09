#! /usr/bin/python

from pymongo import MongoClient
from flask import Flask, json, request, jsonify
from bson.json_util import dumps
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Personalization, Content

URI = "ds253418.mlab.com"
db_50    = MongoClient(URI, 53418)
db_50    = db_50['heroku_z03b9kqp']
db_50.authenticate('concurrency', 'Rwanda@123456')
listings = db_50['listings']
stocks   = db_50['stocks']
users    = db_50['users']
websites = db_50['websites']

api = Flask(__name__)

def send_email():
	message = Mail(
		from_email='crawler@comp50.com',
		to_emails='fbigabiro@gmail.com',
		subject='Sending with Twilio SendGrid is Fun',
		html_content='<strong>and easy to do anywhere, even with Python</strong>')

	sg = SendGridAPIClient('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')
	response = sg.send(message)
	print(response.status_code, response.body, response.headers)

@api.route('/', methods=['GET'])
def get_index():
	return json.dumps('successfully set the app')

@api.route('/get_companies', methods=['GET'])
def get_companies():
	result = []
	for company in listings.find():
		temp = {'name': company['Name'], 'symbol': company['Symbol']}
		result.append(temp)
	return ({ 'data': result }, 200)

@api.route('/get_company_info', methods=['POST'])
def get_company_info():
	req_data = request.json
	name = req_data['name']
	try:
		company = listings.find({'Name': name})
		for cp in company:
			result = {'name': cp['Name'], 'symbol': cp['Symbol']}
		return (result, 200)
	except Exception as e:
		print e
		return ('Could not find company', 404)

@api.route('/add_user', methods=['POST'])
def add_user():
	req_data = request.json
	to = []
	name = req_data['name']
	email = req_data['email']
	watchlist = req_data['watchlist']
	send_email()
	users.insert_one({ 'name': name, 'email': email, 'watchlist': watchlist })
	return ('successfully added user', 200)

@api.route('/add_stock_mentions', methods=['POST'])
def add_stock():
	req_data = request.json
	st_name = req_data['name']
	st_update = req_data['update']
	stocks.update({ 'name': st_name}, { '$push': { 'mentions': { '$each': st_update } }})
	return('successfully added the new mention', 200)

@api.route('/add_watchlist', methods=[''])
def add_watchlist():
	return ('successfully added watchlist', 200)

@api.route('/users', methods=['GET'])
def get_users():
	return json.dumps(user)

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