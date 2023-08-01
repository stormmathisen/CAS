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

@sio.event
def put_value(payload):
    pv = payload['pv']
    value = payload['value']
    print(pv, ': ', value)

@sio.event
def get_buffer(payload):
    pv = payload['pv']
    buffer = payload['buffer']
    timestamps = payload['timestamps']
    print(pv, ': ', len(buffer))
    print(pv, ': ', buffer[-1])
    print(pv, ': ', timestamps[-1])

sio.connect('http://localhost:5000', auth="I am your Father")

#sio.emit('put_value', {'pv': 'CLA-C2V-DIA-BPM-01:X', 'value': 1.234})
#sio.emit('get_value', {'pv': 'CLA-C2V-DIA-BPM-01:X'})
#sio.sleep(2)
sio.emit('get_buffer', {'pv': 'CLA-C2V-DIA-BPM-01:X'})
sio.sleep(10)
sio.disconnect()
