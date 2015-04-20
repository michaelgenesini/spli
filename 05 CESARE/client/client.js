Class("Client", {
    Client: function() {
        this.protocol = "ws://";
        //this.server = "192.168.1.10";//"188.226.236.133";
        //this.port = "10000";
        this.socket = window.WebSocket || window.MozWebSocket;
        if (this.socket == undefined) {
            alert("Socket is not supported");
            this.socket = function() {
                alert("Your browser doesn't support websocket, here!");
            }
        }
        this.canSend = false;
        this.canSendFile = false;

        //holding shouldDecode input
        this.shouldDecode = document.getElementById("shouldDecode");
    },

    init: function() {
        //setting key
        if (!app.key) {
            app.key = prompt("Insert key to decode message. Use 'nope' to avoid decoding");
        }
        //getting server and port value
        server = $('#serverInput').val();
        port = $('#portInput').val();
        if ((!server) || (!port)) {
            alert("Inserisci un server e una porta validi.");
            return;
        }
        app.server = server;
        app.port = port;
        //connecting to websocketserver
        app.connection = new app.socket(app.protocol + app.server + ":" + app.port);
        //setting callbacks
        app.connection.onopen = app.onOpen;
        app.connection.onerror = app.onError;
        app.connection.onmessage = app.onMessage;
        //Setting localhost callbacks
        app.localhost = new app.socket("ws://localhost:"+app.port);
        app.localhost.onopen = app._localhostOpen;
        app.localhost.onerror = app._localhostError;
        app.localhost.onmessage = app._localhostMessage;

        $('#protocol').text(app.protocol);
        $('#server').text(app.server);
        $('#serverport').text(app.port);
    },

    onOpen: function() {
        app.log("Connection is open");
        //we can now send messages
        document.getElementById("input").disabled = false;
        app.canSend = true;
    },

    onError: function(error) {
        app.log("An error occurred");
    },

    // on message received
    onMessage: function(message) {
        // try to decode json (I assume that each message from server is json)
        app.log(message.data);
        if (message.data.indexOf("origin:") != -1) {
            $('#myip').text(message.data.split("origin:")[1]);
        }
    },

    // sending text message
    sendMessage: function() {
        if (app.canSend) {
            var text = $('#input').val() || "";
            if (text != "") {
                app.connection.send(text);
                $('#input').val("");
            } else {
                if (app.canSendFile) {
                    // sending file
                    //key = ($('#key').val() != "") ? parseInt($('#key').val()) : 2;
                    var e = new Crypt(app.text, app.key);
                    var t = e.encode();
                    //console.log(t);
                    //var d = new Decrypt(t, key);
                    //app.decoded = d.decode();
                    app.log("--- ENCODED ---");
                    app.log(t);
                    app.log("--- ENCODED ---");
                    app.connection.send(t);
                    /*
                    var d = new Decrypt(t, key);
                    t = d.decode();
                    app.log("--- DECODED ---");
                    app.log(t);
                    app.log("--- DECODED ---");
                    */
                } else {
                    app.log("Niente da inviare. Inserisci un testo o un file.");
                }
            }
        }
    },

    _localhostError: function(error) {
        app.log("[localhost] an error occurred");
    },

    _localhostMessage: function(message) {
        //key = ($('#key').val() != "") ? parseInt($('#key').val()) : false;
        //while ((key != "nope") || (isNaN(parseInt(key)))) {
            // keep prompting for key until a number or "nope" is inserted
            //key = prompt("Insert key to decode message. Use 'nope' to avoid decoding");
        //}
        if (!app.shouldDecode.checked) {
             app.log("[localhost] " + message.data);
        } else {
            if (app.key == "nope") {
                app.log("[localhost] " + message.data);
            } else {
                //provo a decrittare
                app.log("--- CRYPTED DATA ---");
                app.log(message.data);
                app.log("--- END OF CRYPTED DATA ---");
                var k = parseInt(app.key);
                var d = new Decrypt(message.data, k);
                var t = d.decode();
                app.log("--- DECODED ---");
                app.log(t);
                app.log("--- DECODED ---");
            }
        }
    },

    _localhostOpen: function() {
        app.localhost.send("itsme");
        app.log("[localhost] connected to localhost");
    },

    log: function(data) {
        $('#log').append(data + "<br>");
    }
});

var app;
window.onload = function() {
    app = new Client();
    //set click listeners
    $('#connect').click(app.init);
    $('#send').click(app.sendMessage);

    // setting event listener for file change
    $('#file').change(function(e) {
        app.log("file caricato");
        //Get the first (and only one) file element
        //that is included in the original event
        var file = e.originalEvent.target.files[0],
            reader = new FileReader();
        //When the file has been read...
        reader.onload = function(evt){
            app.text = evt.target.result;
            app.log("--- START FILE ---");
            app.log(app.text);
            app.log("--- END FILE ---");
            app.canSendFile = true;
        };
        //And now, read the file
        reader.readAsText(file);
    });
};