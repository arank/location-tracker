var http = require("http"),
    mongojs = require("mongojs")
    var uri = "mongodb://aran:aran1025@ds047020.mongolab.com:47020/personal-analytics",
    db = mongojs.connect(uri, ["daily_location"]);
    var server = http.createServer(requestHandler);

    function requestHandler(request, response) {
    	response.writeHead(200, {"Content-Type": "application/json"});
    	db.daily_location.find().limit(1).sort({"time": -1}, function(err, records) {
    		if(err) {
			    console.log("There was an error executing the database query.");
			    response.write("null");
			    response.end();
			    return;
			}
			response.write(JSON.stringify(records[0]));
			response.end();
    	});
    }

    server.listen(1234);