Location Tracker Script

For anyone using Android devices, google is pulling your location history and storing it. It can be found at maps.google.com/locationhistory/
This is a quick script for programatically pulling that data and dumping it into a mongo db (meant to be run on a cron job daily). In the config file you can specify the number of points to pull (via the time range of data to gather). This also contains a simple flask api server in app.py to expose gathered data programatically.
