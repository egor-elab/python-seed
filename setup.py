from setuptools import setup

setup(
    name='USBDetector',
    install_requires=[
        'flask',
        'flask_socketio',
        'nameko',
    ],
    tests_require=[
        'pytest',
        'pytest-asyncio',
        'websockets',
    ],
)
