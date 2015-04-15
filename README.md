Location Tracker Script (Originally built for use on arankhanna.com)

For anyone using Android devices, google is pulling your location history and storing it (and it is no longer accessible via Latitude). It can be found at maps.google.com/locationhistory/. This python code allows you to programatically pull an arbitrary subset of that data and dump it into a database (mongo currently) and use a Flask server to expose that data via API endpoints.

To set this up you must:
1) run apache and cofigure it to forward to the Flask server in app.py
2) put mongo database login string in a file named password.conf
3) OPTIONAL: put a google API key in passwords.conf for reverse geocoding and a Mandrill API key for email alerting on failure
3) store your google cookie in a collection named credentials on your database (because this can vary I update it manually in the DB when it changes)
4) OPTIONAL: run json_fetcher.py on a cronjob to pull data regularly into the DB

You can see an example Mapbox-based frontend visualization for the data in the /frontend folder or live at arankhanna.com/contact.html
