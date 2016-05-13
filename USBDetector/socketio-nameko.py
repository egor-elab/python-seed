from functools import partial

import eventlet
from eventlet.event import Event
from eventlet import wsgi
import socketio
from nameko.web import (
    HttpOnlyProtocol,
    WebServer,
    WsgiApp,
)
from nameko.extensions import (
    Entrypoint,
    ProviderCollector,
    SharedExtension,
)


class SocketIOWsgiServer(WebServer):
    def __init__(self):
        super().__init__()
        self._socketio_server = None

    def start(self):
        if not self._starting:
            self._starting = True

            self._socketio_server = socketio.Server()
            self._wsgi_app = socketio.Middleware(self._server, WsgiApp(self))

            self._sock = eventlet.listen(self.bind_addr)
            self._serv = wsgi.Server(
                self._sock,
                self._sock.getsockname(),
                self._wsgi_app,
                protocol=HttpOnlyProtocol,
                debug=False
            )
            self._gt = self.container.spawn_managed_thread(
                self.run, protected=True
            )


class SocketIOServer(SharedExtension, ProviderCollector):
    wsgi_server = SocketIOWsgiServer()

    def handle_request(self, request):
        context_data = self.wsgi_server.context_data_from_headers(request)
        return self.socketio_mainloop(context_data)

    def socketio_mainloop(self, initial_context_data):
        def handler(ws):
            pass
        return WebSocketWSGI(self._socket.handler)

class SocketIORpc(Entrypoint):
    server = SocketIOServer()

    def setup(self):
        self.server.register_provider(self)

    def stop(self):
        self.server.unregister_provider(self)
        super().stop()

    def handle_message(self, socket_id, data, context_data):
        self.check_signature((socket_id,), data)
        event = Event()
        self.container.spawn_worker(
            self, (socket_id,), data,
            context_data=context_data,
            handle_result=partial(self.handle_result, event)
        )

    def handle_result(self, event, worker_ctx, result, exc_info):
        event.send(result, exc_info)
        return result, exc_info


class Example:
    @SocketIORpc.decorator
    def hello(self, data):
        pass
