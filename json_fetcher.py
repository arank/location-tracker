import pycurl, json, datetime, urllib2, ConfigParser, pymongo, urllib2
from io import BytesIO

# TODO add Config to specify how many points to pull and mailer cfg
config = ConfigParser.RawConfigParser()
config.read('/var/www/location-tracker/passwords.cfg')
API_KEY = config.get('google', 'api_key')
MONGODB_URI = config.get('mongo', 'uri')
MANDRILL_KEY = config.get('mandrill', 'api_key')

"""
Gets cookie and other variable credentials from mongo server
"""
def get_google_credentials():
	client = pymongo.MongoClient(MONGODB_URI)
	db = client.get_default_database()
	# TODO check for failure
	creds = db['credentials'].find_one()
	return creds['google-cookie'], creds['google-header']

"""
Converts python datetime to millis from the epoch
"""
def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds() * 1000.0

""" 
Pulls all coordinates (as a list) recorded by your device between the start and end times 
(with both times being express in millis from the epoch) 
"""
def get_coordinates(start_time, end_time):
	data = "[null,"+str(start_time)+","+str(end_time)+",true]"
	out = BytesIO()
	cookie, header = get_google_credentials()
	c = pycurl.Curl()
	c.setopt(c.WRITEFUNCTION, out.write)
	c.setopt(pycurl.URL, "https://maps.google.com/locationhistory/b/0/apps/pvjson?t=0")
	c.setopt(pycurl.HTTPHEADER, 
		['cookie: '+cookie,
		'origin: https://maps.google.com',
		'accept-encoding: application/json',
		'x-manualheader: '+header,
		'accept-language: en-US,en;q=0.8',
		'user-agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'content-type: application/x-www-form-urlencoded;charset=UTF-8',
		'accept: */*',
		'referer: https://maps.google.com/locationhistory/b/0',
		'dnt: 1'])
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, data)
	c.perform()

	try:
		dictionary = json.loads(out.getvalue())
		if(len(dictionary[1]) < 2):
			return None
		else:
			return dictionary[1][1]
	except:
		return None
		
"""
Uses the google geocoding API to get an approximate location for a single latitude and logitude pair
"""
def get_approx_location(lat, lng, max_accuracy=2):
	location = json.load(urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+","+str(lng)+"&key="+API_KEY))
	if(location['status'] == "OK"):	
		accuracy = min(len(location['results'])-1, max_accuracy)
		loc = location['results'][accuracy]
                return loc['formatted_address'], loc['geometry']['location']['lat'], loc['geometry']['location']['lng']
	else:
		return None

"""
Sends a mail to me in case of script failure so I can fix it
"""
# TODO add config to this
def send_failure_mail(log):
	print("sending failure email with log "+log)
	data = {
		"key": MANDRILL_KEY,
		"message": 
		{   "text": log,
			"subject": "Location Tracker Failed",
			"from_email": "arankhanna@college.harvard.edu",
			"from_name": "Location Tracker",
			"to": [{"email": "arankhanna@college.harvard.edu"}]
		},
		"async": "false"
	}
	encoded_data = json.dumps(data)
	# TODO check for failure
	urllib2.urlopen('https://mandrillapp.com/api/1.0/messages/send.json', encoded_data)

"""
Writes arbitary number of data points to a mongo collection
"""
def write_to_mongo(points, collection):
	client = pymongo.MongoClient(MONGODB_URI)
	db = client.get_default_database()
	for point in points:
		# TODO check for failure
		db[collection].insert(point)


# Pull data points from the last 24 hours the last 24
end_time = unix_time(datetime.datetime.now())
start_time = end_time - 86400000 # 24 hours in millis
coordinates = get_coordinates(start_time, end_time)

if coordinates is None:
	send_failure_mail("Failed on google coordinate grab. Try to update credentials at https://mongolab.com/databases/personal-analytics/collections/credentials")
else:
	last_coord = coordinates[len(coordinates)-1]
	location, approx_lat, approx_long = get_approx_location(last_coord[2], last_coord[3])
	if location is None:
		send_failure_mail("failed on google geocoding lookup")
	else:
		print "recorded recent loaction at "+location
		write_to_mongo([{'time': int(last_coord[1]), 'location': location, 'approx-lat': approx_lat, 'approx-long': approx_long}], 'daily_location')
