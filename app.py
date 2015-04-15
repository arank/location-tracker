#!flask/bin/python
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from flask import Flask
import pymongo, json

'''
Simple API server to expose location data scraped into mongodb
'''
# Decorator to allow any domain to access this API
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


'''
List of end points exposing data
'''
app = Flask(__name__)
# Endpoint to get the last (approximate) location recorded by the json_fetcher
@app.route('/location-tracker')
@crossdomain(origin='*')
def index():
    # Log onto mongo host
    client = pymongo.MongoClient("mongodb://aran:aran1025@ds047020.mongolab.com:47020/personal-analytics")
    db = client.get_default_database()

    # Get all data points (exluding database id)
    pts = db['daily_location'].find({}, {'_id': False})
    
    # Return most recent point as a JSON
    last_point = pts[pts.count()-1] 
    j = json.dumps(last_point)
    return str(j)

# Run the App
if __name__ == '__main__':
    app.run(debug=False)
