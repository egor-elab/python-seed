import os

from egor.service.templates import configure, BaseService


LOCALROOT = os.path.abspath(os.path.dirname(__file__))
configuration = configure(
    os.path.join(LOCALROOT, '..'),
    [
    ]
)


class Service(BaseService):
    '''
    '''
    #[[[cog
    #   import cog
    #   cog.outl("name = '{}'".format(service_name))
    #]]]
    #[[[end]]]
