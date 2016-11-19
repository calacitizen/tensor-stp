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
    // userSocket = socket;
});

http.listen(3000, function() {
    console.log('App listening on port 3000!');
});
app.get('/', function(req, res) {

    res.sendfile('index.html')
})

app.get('/ag', function(req, res) {

    res.sendfile('agregator.html')
})

app.post('/push', function(req, res) {
//if (req.body.length < 8) { res.sendStatus(200); return;}

    var result = {
      payLoad: [],
      noteNumbers: [],
      arpArray: [],
      fiveHundreds: false
    }


    var logsCount= req.body.length;
    if (logsCount>8)
      logsCount=8;
    //console.log(logsCount);

    var count500=0;
    var note=0;
    for ( var i=0; i<logsCount; i++) {
      result.payLoad.push(req.body[i]);
      var firstNumberOfSize = req.body[i].size.toString()[0];
      var firstNumberOfAmount =  req.body[i].amount.toString()[0];

      note= Math.abs((+firstNumberOfSize) - (+firstNumberOfAmount));
      if (note>6)
        note=6;
      result.noteNumbers.push(note);

      if (req.body[i].code > 400)
        count500++;
    }

    var arpeggioCount = 0;
    if (logsCount>6)
        arpeggioCount= Math.floor(Math.random() * 4) + 3;
    else
      if (logsCount<=6)
        arpeggioCount= logsCount;

    
    
    for (var i=0; i<arpeggioCount; i++)
    {
      var firstNumberOfSize = req.body[i].size.toString()[0];
      var firstNumberOfAmount =  req.body[i].amount.toString()[0];

      var arp= Math.abs( note - (+firstNumberOfAmount) );
      if (arp>5)
        arp=5;
      result.arpArray.push(arp);
    }

    if (count500>=2)
        result.fiveHundreds= true;

    // userSocket && userSocket.emit('music', result);
    io.sockets.emit('music', result);
    console.log(result);




    res.sendStatus(200);
});
