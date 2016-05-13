from nameko.extensions import DependencyProvider
from nameko.web.websocket import WebSocketHubProvider, rpc


class Config(DependencyProvider):
    def get_dependency(self, worker_ctx):
        return self.container.config


class ContainerIdentifier(DependencyProvider):
    def get_dependency(self, worker_ctx):
        return id(self.container)


class InstrumentManagerProvider:
    pass


class USBDetector:
    name = 'USBDetector'
    config = Config()
    websocket_hub = WebSocketHubProvider()
    instrument_mgr = InstrumentManagerProvider()

    @rpc
    def add_device(self, socket_id, **port_info):
        return self.instrument_mgr.instruments.add(port_info)

    @rpc
    def remove_device(self, socket_id, **port_info):
        return self.instrument_mgr.instruments.remove(port_info)