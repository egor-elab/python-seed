from nameko.extensions import DependencyProvider
from nameko.web.websocket import WebSocketHubProvider, rpc


class Config(DependencyProvider):
    def get_dependency(self, worker_ctx):
        return self.container.config


class ContainerIdentifier(DependencyProvider):
    def get_dependency(self, worker_ctx):
        return id(self.container)


class InstrumentManagerProvider(DependencyProvider):
    class InstrumentCache:
        def __init__(self):
            self.instruments = {}

        def add(self, port_info):
            self.instruments[port_info['deviceName']] = port_info

        def remove(self, port_info):
            del self.instruments[port_info['deviceName']]

    class InstrumentManager:
        def __init__(self):
            self.instruments = self.InstrumentCache()

    def get_dependency(self, worker_ctx):
        return self.InstrumentManager


class Service:
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
