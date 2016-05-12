from jinja2 import Template
from nameko.extensions import DependencyProvider
from nameko.timer import timer
from nameko.web.handlers import http
from nameko.web.websocket import WebSocketHubProvider, rpc
from werkzeug import Response


TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<style>
    #console{
        padding:5px;
        border:1px solid black;
    }
    #console p {
        margin:0;
    }
    .event {
        color:#999;
    }
    .warning{
        color: orange;
    }
</style>
<title>Nameko Websocket Test</title>
</head>
<body>
<div id="wrapper">
    <h1>Nameko Websocket Test</h1>
    <button id="disconnect">Disconnect</button>
    <div id="container">
        <div id="console">
    </div>
</div>
<script type="text/javascript">
    function connect(){
        var socket;
        var host = "ws://{{host}}:{{port}}/ws";
        try{
            var socket = new WebSocket(host);
            message('<p class="event">Socket Status: '+socket.readyState);
            socket.onopen = function(){
                message('<p class="event">Socket Status: '+socket.readyState+' (open)');
                subscribe();
            }
            socket.onmessage = function(msg){
                message('<p class="message">Received: '+msg.data);
            }
            socket.onclose = function(){
                message('<p class="event">Socket Status: '+socket.readyState+' (Closed)');
            }
        } catch(exception){
            message('<p>Error'+exception);
        }
        function subscribe() {
            try{
                var json_msg = `{
                    "method": "subscribe",
                    "data": {}
                }`;
                socket.send(json_msg);
                message('<p class="event">Sent: '+text)
            } catch(exception){
                message('<p class="warning">');
            }
        }
        function message(msg){
            $('#console').append(msg+'</p>');
        }
        $('#disconnect').click(function(){
            socket.close();
        });
    }
    $(document).ready(function() {
        if(!("WebSocket" in window)){
            $('<p>This demo requires browser websocket support</p>').appendTo('#container');
            return
        }
        connect();
    });
</script>
</body>
</html>
"""


class Config(DependencyProvider):
    def get_dependency(self, worker_ctx):
        return self.container.config


class ContainerIdentifier(DependencyProvider):
    def get_dependency(self, worker_ctx):
        return id(self.container)


class WebsocketService(object):
    name = "websockets"

    container_id = ContainerIdentifier()
    websocket_hub = WebSocketHubProvider()
    config = Config()

    @http('GET', '/')
    def home(self, request):
        host = self.config.get('PUBLIC_HOST', 'localhost')
        port = self.config.get('PUBLIC_PORT', '8000')

        payload = Template(TEMPLATE).render({'host': host, 'port': port})
        return Response(payload, content_type="text/html")

    @rpc
    def subscribe(self, socket_id):
        self.websocket_hub.subscribe(socket_id, 'test_channel')
        return 'subscribed to test_channel'

    @timer(10)
    def ping(self):
        print('ping')
        self.websocket_hub.broadcast('test_channel', 'ping', {
            'value': "ping from {}".format(self.container_id),
        })
