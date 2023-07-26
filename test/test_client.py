import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

@sio.event
def auth_success():
    print('auth success')

@sio.event
def auth_fail():
    print('auth fail')

sio.connect('http://localhost:5000', auth="I am your father")
sio.disconnect()
time.sleep(1)
sio.connect('http://localhost:5000', auth="I am NOT your father")
sio.disconnect()

