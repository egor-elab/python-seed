import sys, json
import os
import threading
import time
import subprocess

from collections import deque
from flask import Flask
from flask_socketio import SocketIO, rooms, disconnect
from socketIO_client import LoggingNamespace, SocketIO as SocketIOClient
import requests

LOCALROOT = os.path.dirname(__file__)

def USBDetectorFactory(uri=None, cpath=None):
  app = Flask(__name__)
  io = SocketIO(app) # engineio_logger=True)
  devices = deque()
  roomsList = []
  cpath = cpath or "socketio-client-2.js"


  def die():
    print('kill me')
    io.emit('kill me', {}) #cheating

  class USBDetector:
    def __init__(self, *args, **kwargs):
      self.app = app
      self.io = io
      self.devices = devices
      self.rooms = roomsList
      self.die = die #callable

    #@app.route('/kill')
    #def kill():
     # print('told to kill')
     # io.emit('die', include_self=True)
      #io.emit('bye', include_self=True)

    @io.on('connect')
    def connect():
      print('connection established')
      io.emit('downlink', {'connection': 'good'})
      for rm in rooms():
        roomsList.append(rm)

    @io.on('uplink')
    def uplink(data):
      print('uplink: {}'.format(data))

    @io.on('add')
    def add(device):
      print('server add event')
      devices.append(device)

    @io.on('remove')
    def remove(device):
      print('server remove event')
      devices.remove(device)

    @io.on('disconnect')
    def disconnecting():
      print('disconnecting...')
      disconnect() #emits disconnect message to all clients
      print('all clients are disconnected!')
      io.stop() #raise SystemExit which halts the server
      print('flask app disconnected sucessfully!')

    def pop(self):
      return self.devices.pop()

    def empty(self):
      if(len(self.devices)):
        return False
      return True

    def __enter__(self):
      print("enter")
      self.start()
      return self

    def start(self):
      print('starting')
      self.server_thread = threading.Thread(target=self.run_server)
      self.server_thread.start()
      self.client_thread = threading.Thread(target=self.run_client)
      self.client_thread.start()
      print ('done starting')

    def run_server(self):
      print('running server')
      io.run(app)
      print('done running server')

    def run_client(self):
      print('running client')
      subprocess.call("node "+cpath , shell=True) #move to new function
      print('done running client')

    def __exit__(self, type, value, traceback):
      print('exit due to exception {}'.format(type))
      self.close()

    def close(self):
      print('closing')
      self.die()
      self.server_thread.join()
      self.client_thread.join()
      print('joined')

  return USBDetector

if __name__ == '__main__':
  with USBDetectorFactory()() as usb:
    print("sleep")
    time.sleep(10);
    print("wakeup")
    print(usb.devices)
  print ('done')


