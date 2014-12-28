import pycurl, json, datetime, urllib2, ConfigParser
from io import BytesIO

config = ConfigParser.RawConfigParser()
config.read('passwords.cfg')
API_KEY = config.get('google', 'api_key')
COOKIE = config.get('google', 'cookie')

"""
Converts python datetime to millis from the epoch
"""
def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds() * 1000.0

# TODO send alert on cookie/api_key expiration
""" 
Pulls all coordinates recorded by your device between the start and end times 
(with both times being express in millis from the epoch) 
"""
def get_coordinates(start_time, end_time):
	data = "[null,"+str(start_time)+","+str(end_time)+",true]"
	out = BytesIO()
	c = pycurl.Curl()
	c.setopt(c.WRITEFUNCTION, out.write)
	c.setopt(pycurl.URL, "https://maps.google.com/locationhistory/b/0/apps/pvjson?t=0")
	c.setopt(pycurl.HTTPHEADER, 
		['cookie: '+COOKIE,
		'origin: https://maps.google.com',
		'accept-encoding: application/json',
		'x-manualheader: lBgJkp-_phUYxrlgPUKyP_KRkmY:1419717526596',
		'accept-language: en-US,en;q=0.8',
		'user-agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'content-type: application/x-www-form-urlencoded;charset=UTF-8',
		'accept: */*',
		'referer: https://maps.google.com/locationhistory/b/0',
		'dnt: 1'])
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, data)
	c.perform()

	dictionary = json.loads(out.getvalue())
	return dictionary[1][1]

"""
Uses the google geocoding API to get an approximate location for a single latitude and logitude pair
"""
def get_approx_location(lat, lng):
	location = json.load(urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+","+str(lng)+"&key="+API_KEY))
	return location['results'][2]['formatted_address']

# def write_to_db():



today = datetime.date.today()
end_time = unix_time(datetime.datetime.combine(today, datetime.datetime.min.time()))
start_time = end_time - 86400000 # 24 hours in millis
# list of all lat-long values
coordinates = get_coordinates(start_time, end_time)
print coordinates
# TODO write coordinates to DB
last_coord = coordinates[len(coordinates)-1]
location = get_approx_location(last_coord[2], last_coord[3])
# TODO write approx location to DB
print location
