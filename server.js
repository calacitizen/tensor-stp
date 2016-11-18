var express = require('express');
var app = express();
var socketio = require('socket.io');

var bodyParser = require('body-parser');


app.use(bodyParser.json())


app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});

app.post('/push', function(req, res){
    console.log(req.body)



    res.sendStatus(200);
})

