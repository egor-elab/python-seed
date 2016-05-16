from nameko.extensions import DependencyProvider


class Config(DependencyProvider):
    def get_dependency(self, worker_ctx):
        return self.container.config


class Service:
    #[[[cog
    #   import cog
    #   cog.outl("name = '{}'".format(service_name))
    #]]]
    name = "scaffolded"
    #[[[end]]]

    config = Config()
