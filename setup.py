from setuptools import setup, find_packages

setup(
    #[[[cog
    #   cog.outl("name='{}',".format(service_name))
    #]]]
    #[[[end]]]
    packages=find_packages(),
    install_requires=[
        'nameko',
        'egor',
    ],
    dependency_links = [
        'https://github.com/egor-elab/egor/tarball/master#egg=egor'
    ],
    tests_require=['tox'],
)
