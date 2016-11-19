var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var bodyParser = require('body-parser');

var userSocket = null;

app.use(bodyParser.json())
app.get('/', function(req, res) {
    res.sendfile('index.html');
});

app.use(express.static(__dirname + '/public'));

io.on('connection', function(socket) {
    userSocket = socket;
});

app.listen(3000, function() {
    console.log('App listening on port 3000!');
});
app.get('/', function(req, res) {

    res.sendfile('index.html')
})

app.get('/ag', function(req, res) {

    res.sendfile('agregator.html')
})

app.post('/push', function(req, res) {

    userSocket && userSocket.emit('music', req.body)
    //res.send(req.body);
    res.sendStatus(200);
});