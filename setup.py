from setuptools import setup, find_packages

setup(
#[[[cog
#   import cog
#   import json
#   config = json.load('scaffold.json')
#   cog.outl('name={}'.format(config.name))
#]]]
#[[[end]]]
    packages=find_packages(),
    install_requires=[
        'nameko',
    ],
    tests_require=['tox'],
)
