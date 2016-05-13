var socket = new WebSocket('ws://localhost:8000/ws');
socket.onopen = function () {
  console.log('socket open');
  socket.send(JSON.stringify({ method: 'subscribe', data: {} }));
};
socket.onmessage = function (msg) {
  console.log('rxed: ', msg);
};
socket.onclose = function () {
  console.log('socket closed');
};
