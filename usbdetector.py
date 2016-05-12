import json

from nameko.extensions import DependencyProvider
from nameko.web.websocket import WebSocketHubProvider, rpc


class Config(DependencyProvider):
    def get_dependency(self, worker_ctx):
        return self.container.config


class ContainerIdentifier(DependencyProvider):
    def get_dependency(self, worker_ctx):
        return id(self.container)


class USBDetector:
    name = 'USBDetector'
    config = Config()
    websocket_hub = WebSocketHubProvider()

    @rpc
    def subscribe(self, value):
        return 'got subscription msg'
