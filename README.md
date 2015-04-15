Location Tracker Script

For anyone using Android devices, google is pulling your location history and storing it. It can be found at maps.google.com/locationhistory/. This python code allows you to programatically pull an arbitrary subset of that data and dump it into a database (mongo currently) and use a Flask server to expose that data via API endpoints.

This is currently being used on my website (also open source) at arankhanna.com/contact

In the config file you can specify the number of points to pull (via the time range of data to gather). This also contains a simple flask api server in app.py to expose gathered data programatically.
