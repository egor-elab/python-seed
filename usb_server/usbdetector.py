import sys, json
import os
import threading
import time
import subprocess

from collections import deque
from flask import Flask
from flask_socketio import SocketIO, rooms, disconnect, emit
import flask_socketio as fsio
from socketIO_client import LoggingNamespace, SocketIO as SocketIOClient
import requests

LOCALROOT = os.path.dirname(__file__)

def USBDetectorFactory(uri=None, cpath=None):
  app = Flask(__name__)
  io = SocketIO(app) #,engineio_logger=True) #message_queue="redis://localhost:5000")
  new_devices = deque()
  removed_devices = deque()
  roomsList = []
  cpath = cpath or "socketio-client-2.js"


  def die():
    print(roomsList)
    sid = roomsList[0]
    #io.emit('Hi', {})
    #print('sid: ', sid)
    io.emit('Hi', room=sid )


  class USBDetector:
    def __init__(self, *args, **kwargs):
      self.app = app
      self.io = io
      self.new_devices = new_devices
      self.removed_devices = removed_devices
      self.rooms = roomsList
      self.die = die #callable

    @io.on('connect')
    def connect():
      print('connection with the server established')
      io.emit('downlink', {'connection': 'good'})
      for rm in rooms():
        roomsList.append(rm)

    @io.on('uplink')
    def uplink(data):
      print('uplink: {}'.format(data))

    @io.on('add')
    def add(device):
      print('server add event')
      new_devices.append(device)

    @io.on('remove')
    def remove(device):
      print('server remove event')
      removed_devices.append(device)

    @io.on('disconnect')
    def disconnecting():
      print('disconnecting server...')
      disconnect() #emits disconnect message to all clients
      print('all clients are disconnected!')
      io.stop() #raise SystemExit which halts the server
      print('flask app disconnected sucessfully!')

    def __enter__(self):
      self.start()
      return self

    def start(self):
      self.server_thread = threading.Thread(target=self.run_server)
      self.server_thread.start()

      self.client_thread = threading.Thread(target=self.run_client)
      self.client_thread.start()

    def run_server(self):
      io.run(app)
      print('done running server')

    def run_client(self):
      subprocess.call("node "+cpath , shell=True) #move to new function
      print('done running client')

    def __exit__(self, type, value, traceback):
      if type == None:
        print('usb detector exit due to exception {}'.format(type))
      self.close()

    def close(self):
      #self.die()
      #io.stop() #raise SystemExit which halts the server
      print('ERROR: unable to shut down the server!')
      self.client_thread.join()
      print('clients disconnected successfuly')
      self.server_thread.join()
      print('server disconnected successfuly')

  return USBDetector

if __name__ == '__main__':
  with USBDetectorFactory()() as usb:
    time.sleep(2);
  print ('done')


