Location Tracker Script (Originally built for use on arankhanna.com)

For anyone using Android devices, google is pulling your location history and storing it. It can be found at maps.google.com/locationhistory/. This python code allows you to programatically pull an arbitrary subset of that data and dump it into a database (mongo currently) and use a Flask server to expose that data via API endpoints.

To set this up you must:
1) run apache and cofigure it to forward to the Flask server in app.py
2) mongo database login credentials and a google api key in a file named password.conf
3) store your google cookie in a collection on your database (because this can vary I update it manually when it changes)
4) OPTIONAL: run json_fetcher.py on a cronjob to pull data regularly into the DB

You can see an example Mapbox-based frontend visualization for the data in the /frontend folder or live at arankhanna.com/contact.html
