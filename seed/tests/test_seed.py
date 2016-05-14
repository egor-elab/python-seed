import pytest
from nameko.testing.services import replace_dependencies

#[[[cog
#   import cog
#   cog.outl('from {name}.Service import Service'.format(name=service_name))
#]]]
from scaffolded.Service import Service
#[[[end]]]


@pytest.yield_fixture
def container(container_factory, web_config):
    container = container_factory(Service, web_config)
    container.start()
    yield container


class TestService:
    def test_up(self, container):
        pass
