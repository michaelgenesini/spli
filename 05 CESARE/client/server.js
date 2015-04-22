// 02 example
// websocket RFC 6455

var ws = require("websocket"),
    http = require("http");

var wsServerConstructor = ws.server;

var PORT = 10000;

//http server
var httpserver = http.createServer(function(req, res) {});
httpserver.listen(PORT, function() {
    console.log("Server is listening on port: " + PORT);
});


//websocket server
var server = new wsServerConstructor({
    httpServer: httpserver
});

var mysocket, other;

server.on('request', function(request) {
    var connection = request.accept(null, request.origin);

    console.log("Server got connection from: " + request.host);
    connection.send("origin:"+request.host);

    connection.on('message', function(message) {
        if (message.type === 'utf8') {
            // process WebSocket message
            console.log(message.utf8Data);
            if (message.utf8Data.indexOf("itsme") != -1) {
                mysocket = connection;
                mysocket.send("hi!");
            } else {
                connection.send("Message received: " + message.utf8Data);
                if (mysocket) {
                    mysocket.send(message.utf8Data);
                }
            }
        }
    });

    connection.on('close', function(connection) {
        // close user connection
    });
});





