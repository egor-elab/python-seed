import asyncio
import json
import websockets

import pytest
from nameko.testing.services import worker_factory

from USBDetector import USBDetector


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
        async def __aenter__(self):
            self.socket = await websockets.connect('ws://localhost:8000/ws')
            return self

        async def __aexit__(self, exc_type, exc_value, traceback):
            pass

        async def add(name):
            await websockets.send(json.dumps(dict(
                deviceName=name
            )))

    return Client()


class TestUSBDetector:
    @pytest.mark.asyncio
    async def test_add_remove(self, instrument_mgr, websocket_client):
        print('test add remove')
        self.service = worker_factory(
            USBDetector,
            instrument_mgr=instrument_mgr
        )
        self.client = websocket_client()

        async with self.client as client:
            client.add('COM3')
            client.add('COM6')
            client.remove('COM3')
            client.add('COM8')
        assert len(self.service.instrument_mgr.instruments) == 2

# async def _add_remove(instrument_mgr, websocket_client):
#     service = worker_factory(
#         USBDetector,
#         instrument_mgr=instrument_mgr
#     )
#     client = websocket_client()

#     async with client as cl:
#         cl.add('COM3')
#         cl.add('COM6')
#         cl.remove('COM3')
#         cl.add('COM8')
#     assert len(service.instrument_mgr.instruments) == 2
