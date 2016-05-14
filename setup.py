from setuptools import setup, find_packages

setup(
    #[[[cog
    #   cog.outl('name="{}",'.format(service_name))
    #]]]
    name="scaffolded",
    #[[[end]]]
    packages=find_packages(),
    install_requires=[
        'nameko',
    ],
    tests_require=['tox'],
)
