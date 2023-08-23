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
    pv = payload['pv_name']
    value = payload['value']
    print(pv, ': ', value)

@sio.event
def put_value(payload):
    pv = payload['pv_name']
    value = payload['new_value']
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
    pv = payload['pv_name']
    value = payload['value']
    time= payload['timestamp']
    print('New value:', pv, ': ', value, "at", time)


@sio.event
def list_monitors(payload):
    print("Monitor list:")
    print(payload)

@sio.event
def validation_error(payload):
    print(payload)

sio.connect(f'http://{ip}:5000', auth="I am your Father")
# print("Putting to monitored value")
# sio.emit('put_value', {'pv': 'CLA-C2V-DIA-BPM-01:X', 'value': 1.234})
# sio.sleep(1)
# sio.emit('put_value', {'pv_name': 'CLA-C2V-DIA-BPM-01:X', 'new_value': 1.234})
# sio.sleep(1)
# print("Putting to fallback values")
# sio.emit('put_value', {'pv': 'CLA-S01-DIA-BPM-01:X', 'value': 5.678})
# sio.sleep(1)
# sio.emit('put_value', {'pv_name': 'CLA-S01-DIA-BPM-01:X', 'new_value': 5.678})
# sio.sleep(1)
# print('Getting values')
# sio.emit('get_value', {'pv_name': 'CLA-C2V-DIA-BPM-01:X'})
# sio.sleep(1)
# sio.emit('get_value', {'pv_name': 'CLA-S01-DIA-BPM-01:X'})
# sio.sleep(2)
for i in range(250):
    sio.emit('put_value', {'pv_name': 'CLA-C2V-DIA-BPM-01:X', 'new_value': i})
    sio.sleep(0.1)
print('Getting buffers')
# sio.emit('start_monitor', {'pv': 'CLA-S01-DIA-BPM-01:X', 'length': 10})
sio.emit('get_buffer', {'pv_name': 'CLA-C2V-DIA-BPM-01:X', 'buffer_size': 10})
# sio.sleep(1)
# sio.emit('subscribe', {'pv': 'CLA-C2V-DIA-BPM-01:X'})
# sio.emit('put_value', {'pv_name': 'CLA-C2V-DIA-BPM-01:X', 'new_value': 12.345})
# sio.emit('put_value', {'pv_name': 'CLA-C2V-DIA-BPM-01:X', 'new_value': 23.456})
# sio.emit('put_value', {'pv_name': 'CLA-C2V-DIA-BPM-01:X', 'new_value': 34.567})
sio.sleep(2)
# sio.emit('unsubscribe', {'pv': 'CLA-C2V-DIA-BPM-01:X'})
# sio.emit('subscribe', {'pv': 'CLA-S01-DIA-BPM-01:X'})
# sio.emit('get_buffer', {'pv': 'CLA-C2V-DIA-BPM-01:X'})
# sio.sleep(1)
# sio.emit('list_monitors', {})
# sio.sleep(1)
# sio.emit('get_buffer', {'pv': 'CLA-S01-DIA-BPM-01:X'})
# sio.emit('stop_monitor', {'pv': 'CLA-S01-DIA-BPM-01:X'})
# sio.sleep(1)
sio.disconnect()
