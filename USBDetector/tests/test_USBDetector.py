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
    yield container


class TestUSBDetector:
    def test_connect(self, container, websocket):
        container.start()
        websocket()

    def test_add_remove(self, container, websocket_client):
        _instruments = {}

        mock_mgr = replace_dependencies(container, 'instruments')
        mock_mgr.add.side_effect = lambda dev: _instruments.setdefault(dev['deviceName'], {})
        mock_mgr.add.return_value = 'added'
        mock_mgr.remove.side_effect = lambda dev: _instruments.pop(dev['deviceName'])
        mock_mgr.remove.return_value = 'removed'

        container.start()

        client = websocket_client()
        client.add('COM3')
        client.add('COM6')
        client.remove('COM3')
        client.add('COM8')
        assert len(_instruments) == 2
