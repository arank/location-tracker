var http = require("http"),
    mongojs = require("mongojs")
    var uri = "mongodb://aran:aran1025@ds047020.mongolab.com:47020/personal-analytics",
    db = mongojs.connect(uri, ["daily_location"]);
    var server = http.createServer(requestHandler);

    // TODO uncomment this when url controller is set up!!!!!
   //  function requestHandler(request, response) {
   //  	response.writeHead(200, {"Content-Type": "application/json"});
   //  	db.daily_location.find().limit(1).sort({"time": -1}, function(err, records) {
   //  		if(err) {
			//     console.log("There was an error executing the database query.");
			//     response.write("none");
			//     response.end();
			//     return;
			// }
   //          var date = new Date(records[0]['time']);
			// response.write(JSON.stringify({'location':records[0]['location'], 'time': date.toString()}));
			// response.end();
   //  	});
   //  }

    function requestHandler(request, response){
        response.writeHead(200, {"Content-Type": "application/json"});
        var exec = require('child_process').exec;
        exec('python /home/ubuntu/Projects/location\ tracker/api_server/cookie_refresher.py', 
            function (error, stdout, stderr) {
                // Possibly do something with stdout
            });
        response.end()
    } 

    server.listen(5555);