#!flask/bin/python
from flask import Flask
import pymongo, ConfigParser

app = Flask(__name__)

config = ConfigParser.RawConfigParser()
config.read('passwords.cfg')
MONGODB_URI = config.get('mongo', 'uri')	

@app.route('/last-location')
def index():
    client = pymongo.MongoClient(MONGODB_URI)
	db = client.get_default_database()
	creds = db['daily_location'].find_one()
	return str(creds)

if __name__ == '__main__':
    app.run(debug=True)