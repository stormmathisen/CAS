import eventlet
from eventlet import wsgi
import socketio
import config


config = config.Config(".\\server\\config.yaml")

verbose = True

import os
import sys

if config.epics['set-env']:
    os.environ["EPICS_CA_ADDR_LIST"] = config.epics['addr-list']
    os.environ["EPICS_CA_AUTO_ADDR_LIST"] = config.epics['auto-addr']
    os.environ["EPICS_CA_SERVER_PORT"] = config.epics['server-port']
    import epics
else:
    import epics
sys.path.append("C:\\dev\\python\\apps\\clara\\machine")
from pv import PVBuffer, PVArrayBuffer

def start_monitors(pvs):
    for pv in pvs:
        if config.epics['state'].lower() == "virtual":
            pv = "VM-" + pv
        PV_list[pv] = PVBuffer(pv)

def check_auth(client_ip, secret):
    if secret in config.auth['api-keys']:
        return True
    if client_ip in config.auth['ip-list']:
        return True
    else:
        return False

PV_list = {}
Client_list = {}

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ, auth):
    new_client = {}
    new_client['sid'] = sid
    new_client['ip'] = environ['REMOTE_ADDR']
    if check_auth(environ['REMOTE_ADDR'], auth):
        new_client['auth'] = auth
        Client_list[sid] = new_client
        sio.emit('auth_success', room=sid)
        if verbose: print(f'Client {Client_list[sid]["sid"]} connected from {Client_list[sid]["ip"]}')
    else:
        new_client['auth'] = None
        Client_list[sid] = new_client
        sio.emit('auth_fail', room=sid)
        if verbose: print(f'Client {Client_list[sid]["sid"]} refused from {Client_list[sid]["ip"]}')
        sio.disconnect(sid)
    #TODO: Log the connection

@sio.event
def disconnect(sid):
    if verbose: print(f'Client {Client_list[sid]["sid"]} disconnected from {Client_list[sid]["ip"]}')
    Client_list.pop(sid)
    #TODO: Log the disconnection

@sio.event
def get_value(sid, payload):
    pv = payload["pv"]
    if verbose: print(f'Client {Client_list[sid]["sid"]} requested value of {pv}')
    if config.epics['state'].lower() == "virtual":
        pv = "VM-" + pv
    if pv in PV_list.keys():
        value = PV_list[pv].value
    else:
        value = epics.caget(pv)
    sio.emit('get_value', {'pv': pv, 'value': value}, room=sid)

@sio.event
def put_value(sid, payload):
    pv = payload["pv"]
    value = payload["value"]
    if verbose: print(f'Client {Client_list[sid]["sid"]} requested to put {value} to {pv}')
    if config.epics['state'].lower() == "virtual":
        pv = "VM-" + pv
    if pv in PV_list.keys():
        PV_list[pv].value = value
    else:
        epics.caput(pv, value)
    sio.emit('put_value', {'pv': pv, 'value': value}, room=sid)

@sio.event
def get_buffer(sid, payload):
    pv = payload["pv"]
    if verbose: print(f'Client {Client_list[sid]["sid"]} requested buffer of {pv}')
    if config.epics['state'].lower() == "virtual":
        pv = "VM-" + pv
    if pv in PV_list:
        buffer = list(PV_list[pv].getBuffer())
        print(len(buffer))
        print(buffer)
        timestamps = list(PV_list[pv].getTimeBuffer())
        sio.emit('get_buffer', {'pv': pv, 'buffer': buffer, 'timestamps': timestamps}, room=sid)

if __name__ == '__main__':
    #TODO: Log the start of the server
    start_monitors(config.epics['pv-list'])
    wsgi.server(eventlet.listen((config.server['ip'], config.server['port'])), site=app)