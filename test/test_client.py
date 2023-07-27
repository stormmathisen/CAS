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

@sio.event
def get_value(payload):
    pv = payload['pv']
    value = payload['value']
    print(pv, ': ', value)

sio.connect('http://localhost:5000', auth="I am your father")

sio.emit('get_value', {'pv': 'CLA-C2V-DIA-BPM-01:X'})
sio.sleep(2)
sio.disconnect()
