// var io = require('socket.io-client') ;
// var socket = io.connect('http://localhost:5000', {transports: ['websocket']});
var WebSocket = require('ws');
var usbDetect = require('usb-detection');

var socket = new WebSocket('ws://localhost:8000/ws');

socket.onopen = function () {
  console.log('client is connected');

  /****** usb detection ******/
  usbDetect.on('add', function(device) {
    console.log('adding ', device);
    socket.send(
      JSON.stringify(
        {
          method: 'add_device',
          data: device
        }
      )
    );
  });


  usbDetect.on('remove', function(device) {
    console.log('removing ', device);
    socket.send(
      JSON.stringify(
        {
          method: 'remove_device',
          data: device
        }
      )
    );
  });
};

socket.onmessage = function (msg) {
  console.log('rxed: ', msg.data);
};

socket.onclose = function () {
  console.log('disconnecting client...');
  usbDetect.stopMonitoring();
  console.log('usb dtection disconnected successfully!');

  //socket.disconnect(); //halts the client thread
};
