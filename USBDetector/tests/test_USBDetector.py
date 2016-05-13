import websockets

import pytest
from nameko.testing.services import replace_dependencies

from USBDetector.USBDetector import Service


@pytest.fixture
def instrument_mgr():
    class InstrumentCache:
        def __init__(self):
            self.instruments = {}

        def add(self, port_info):
            self.instruments[port_info['deviceName']] = port_info

        def remove(self, port_info):
            del self.instruments[port_info['deviceName']]

    class InstrumentManager:
        def __init__(self):
            self.instruments = InstrumentCache()

    return InstrumentManager


@pytest.fixture
def websocket_client():
    class Client:
        def __init__(self, websocket):
            self.ws = websocket()

        def add(self, name):
            self.ws.rpc('add_device', deviceName=name)

        async def remove(self, name):
            self.ws.rpc('remove_device', deviceName=name)

    return Client


@pytest.yield_fixture
def container(container_factory, web_config):
    container = container_factory(Service, web_config)
    container.start()
    yield container


class TestUSBDetector:
    def test_connect(self, container, websocket):
        websocket()

    # @pytest.mark.asyncio
    # async def test_add_remove(self, container, instrument_mgr, websocket):
    #     replace_dependencies(container,
    #     self.service = worker_factory(
    #         Service,
    #         instrument_mgr=instrument_mgr
    #     )

    #     async with self.client as client:
    #         client.add('COM3')
    #         client.add('COM6')
    #         client.remove('COM3')
    #         client.add('COM8')
    #     assert len(self.service.instrument_mgr.instruments) == 2
