from nameko.extensions import DependencyProvider

from egor.service.templates import BaseService


class Service(BaseService):
    #[[[cog
    #   import cog
    #   cog.outl("name = '{}'".format(service_name))
    #]]]
    #[[[end]]]
