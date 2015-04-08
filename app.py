#!flask/bin/python
from flask import Flask, jsonify
import pymongo, ConfigParser

app = Flask(__name__)

config = ConfigParser.RawConfigParser()
config.read('passwords.cfg')
MONGODB_URI = config.get('mongo', 'uri')	

@app.route('/last-location', methods=['GET'])
def get_last_location():
    client = pymongo.MongoClient(MONGODB_URI)
	db = client.get_default_database()
	creds = db['daily_location'].find_one()
	return jsonify(creds)

if __name__ == '__main__':
    app.run(debug=True)