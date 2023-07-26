import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')
    exit()

@sio.event
def auth_success():
    print('auth success')

@sio.event
def auth_fail():
    print('auth fail')

sio.connect('http://localhost:5000', auth="I am your father")
sio.disconnect()