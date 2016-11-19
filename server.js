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
    

    var result = {
      payLoad: [],
      noteNumbers: [],    
      arpArray: [],        
      fiveHundreds: false
    }

    

    var count500=0;
    for ( var i=0; i<8; ++i) {
      result.payLoad.push(req.body[i]);
      var firstNumberOfSize = req.body[i].size.toString()[0];
      var firstNumberOfAmount =  req.body[i].amount.toString()[0];
      
      var note= Math.abs((+firstNumberOfSize) - (+firstNumberOfAmount));
      if (note>7)
        note=7;
      result.noteNumbers.push(note);

      if (req.body[i].code > 400)
        count500++;
    }

    for (var i=0; i<6; ++i)
    {
      var firstNumberOfSize = req.body[i].size.toString()[0];
      var firstNumberOfAmount =  req.body[i].amount.toString()[0];
     
      var note= Math.abs( (+firstNumberOfSize) - (+firstNumberOfAmount));
      if (note>5)
        note=5;
      result.arpArray.push(note);
    }
      
    if (count500>=2)
        result.fiveHundreds= true;

    console.log(result.noteNumbers);
    console.log(result.arpArray);
    console.log(result.fiveHundreds);

    userSocket && userSocket.emit('music', result);





    res.sendStatus(200);
});