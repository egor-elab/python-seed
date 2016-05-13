from setuptools import setup, find_packages

setup(
#[[[cog
#   import cog
#   import json
#   with open('scaffold.json', 'r') as f:
#       config = json.load(f)
#   cog.outl('name={}'.format(config['name']))
#]]]
#[[[end]]]
    packages=find_packages(),
    install_requires=[
        'nameko',
    ],
    tests_require=['tox'],
)
