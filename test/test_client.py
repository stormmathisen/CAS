import socketio
import time
import sys

n = sys.argv
if len(n) > 1:
    ip = n[1]
else:
    ip = 'localhost'

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

@sio.event
def auth_success(data):
    print(data)
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

@sio.event
def new_value(payload):
    pv = payload['pv']
    value = payload['value']
    print(pv, ': ', value)


@sio.event
def list_monitors(payload):
    print("Monitor list:")
    print(payload)

sio.connect(f'http://{ip}:5000', auth="I am your Father")

#sio.emit('put_value', {'pv': 'CLA-C2V-DIA-BPM-01:X', 'value': 1.234})
#sio.emit('get_value', {'pv': 'CLA-C2V-DIA-BPM-01:X'})
#sio.sleep(2)
sio.emit('start_monitor', {'pv': 'CLA-S01-DIA-BPM-01:X', 'length': 10})
sio.emit('get_buffer', {'pv': 'CLA-C2V-DIA-BPM-01:X'})
sio.sleep(1)
sio.emit('subscribe', {'pv': 'CLA-C2V-DIA-BPM-01:X'})
sio.sleep(1)
sio.emit('unsubscribe', {'pv': 'CLA-C2V-DIA-BPM-01:X'})
sio.emit('subscribe', {'pv': 'CLA-S01-DIA-BPM-01:X'})
sio.emit('get_buffer', {'pv': 'CLA-C2V-DIA-BPM-01:X'})
sio.sleep(1)
sio.emit('list_monitors', {})
sio.sleep(1)
sio.emit('get_buffer', {'pv': 'CLA-S01-DIA-BPM-01:X'})
sio.emit('stop_monitor', {'pv': 'CLA-S01-DIA-BPM-01:X'})
sio.sleep(1)
sio.disconnect()
