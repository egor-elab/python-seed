import pytest
from USBDetector.USBDetector import Service
from nameko.testing.services import replace_dependencies


@pytest.fixture
def websocket_client(websocket):
    class Client:
        def __init__(self):
            self.ws = websocket()

        def add(self, name):
            return self.ws.rpc('add_device', deviceName=name)

        def remove(self, name):
            return self.ws.rpc('remove_device', deviceName=name)

    return Client


@pytest.yield_fixture
def container(container_factory, web_config):
    container = container_factory(Service, web_config)
    container.start()
    yield container


instruments = {}


@pytest.yield_fixture
def instrument_mock(container_factory, web_config):
    container = container_factory(Service, web_config)

    def add(dev):
        instruments[dev['deviceName']] = dev

    def remove(dev):
        removed = instruments.pop(dev['deviceName'])
        return removed

    mock = replace_dependencies(container, 'instruments')
    mock.add = add
    mock.remove = remove

    container.start()
    yield container


class TestUSBDetector:
    def test_connect(self, container, websocket):
        websocket()

    def test_add_remove(self, instrument_mock, websocket_client):
        client = websocket_client()
        client.add('COM3')
        client.add('COM6')
        client.remove('COM3')
        client.add('COM8')
        assert len(instruments) == 2
