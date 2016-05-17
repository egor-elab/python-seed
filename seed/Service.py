import os

from nameko.extensions import DependencyProvider

from egor.service.templates import configure, BaseService


configuration = configure(
    os.path.join(LOCALROOT, '..'),
    [
    ]
)

class Service(BaseService):
    #[[[cog
    #   import cog
    #   cog.outl("name = '{}'".format(service_name))
    #]]]
    #[[[end]]]
