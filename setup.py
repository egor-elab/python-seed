from setuptools import setup, find_packages

setup(
    name='USBDetector',
    packages=find_packages(),
    install_requires=[
        'nameko',
    ],
    tests_require=['tox'],
)
