var io = require('socket.io-client') ; 
var socket = io.connect('http://localhost:5000', {transports: ['websocket']});
var usbDetect = require('usb-detection');


/****** client.js ******/
socket.on('connect', function () {
  console.log('connected');
  socket.emit('uplink', {'from': 'node'});


  /****** usb detection ******/
  usbDetect.on('add', function(device) {
    socket.emit('add', device);
    console.log('client add event');
  });

  usbDetect.on('remove', function(device) {
    socket.emit('remove', device);
    console.log('client remove event');
  });

});

socket.on('disconnect', function() {
  console.log('disconnecting client...');
  usbDetect.stopMonitoring();
  console.log('usb dtection disconnected successfully!');
  socket.disconnect(); //halts the client thread
  console.log('socket disconnected successfully!');
});

socket.on('downlink', function (data) {
  console.log('downlink: ', data);
});

socket.on('Hi', function (data) {
  console.log('downlink: ', data);
});
