// var WebSocket = require('ws');

// var socket = new WebSocket('ws://localhost:8000/ws');
// socket.onopen = function () {
//   console.log('open');
//   socket.send('{"method": "subscribe", "data": {}}');
// };

// socket.onmessage = function (msg) {
//   console.log('rxed: ', msg);
// };

var io = require('socket.io-client');
var socket = io.connect('ws://localhost:8000/ws', {transports: ['websocket']});

socket.on('connect', function () {
  console.log('connected');
});
