import eventlet
from eventlet import wsgi
import socketio
import config
import payload
from pydantic import ValidationError
from time import time


config = config.Config(".//server//config.yaml")

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

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


import epics_interface as EI

def start_monitors(pvs):
    for pv in pvs:
        if config.epics['state'].lower() == "virtual":
            pv = "VM-" + pv
        PV_list[pv] = EI.PVInterface(pv, nf=send_new)
        PV_list[pv].writeAccess = True
        PV_list[pv].pv.connect()

def check_auth(client_ip, secret):
    if secret in config.auth['api-keys']:
        return True
    if client_ip in config.auth['ip-list']:
        return True
    else:
        return False

PV_list = {}
Client_list = {}


@sio.event
def connect(sid, environ, auth):
    new_client = {}
    new_client['sid'] = sid
    new_client['ip'] = environ['REMOTE_ADDR']
    if check_auth(environ['REMOTE_ADDR'], auth): #If authentication successful
        new_client['auth'] = auth
        Client_list[sid] = new_client
        data = payload.auth_out(
            server_name=config.server['name'],
            auth=True,
            clients=len(Client_list),
            monitors=list(PV_list.keys())
        ).model_dump()
        sio.emit('auth_success', room=sid, data=data)
        if verbose: print(f'Client {Client_list[sid]["sid"]} connected from {Client_list[sid]["ip"]}')
    else: #If not authenticated, refuse connection
        new_client['auth'] = None
        Client_list[sid] = new_client
        data = payload.auth_out(
            server_name=config.server['name'],
            auth=False,
            clients=-1,
            monitors=[]
        ).model_dump()
        sio.emit('auth_fail', data=data, room=sid)
        if verbose: print(f'Client {Client_list[sid]["sid"]} refused from {Client_list[sid]["ip"]}')
        sio.disconnect(sid)
    #TODO: Log the connection

@sio.event
def disconnect(sid):
    if verbose: print(f'Client {Client_list[sid]["sid"]} disconnected from {Client_list[sid]["ip"]}')
    Client_list.pop(sid)
    #TODO: Log the disconnection

@sio.event
def get_value(sid, data):
    try:
        data_in = payload.get_value_in(**data)
    except ValidationError  as e:
        print(f'Client {Client_list[sid]["sid"]} sent invalid payload')
        sio.emit('validation_error', {'error': e.errors()}, room=sid)
        return
    pv = data_in.pv_name
    if verbose: print(f'Client {Client_list[sid]["sid"]} requested value of {pv}')
    if config.epics['state'].lower() == "virtual":
        pv = "VM-" + pv
    try: #This is faster than checking if the PV exists in the dictionary
        value = PV_list[pv].value
        data = payload.get_value_out(
            server_name=config.server['name'],
            pv_name=pv,
            value=value,
            timestamp=PV_list[pv].time,
            fallback=False
        ).model_dump()

    except KeyError:
        value = epics.caget(pv)
        data = payload.get_value_out(
            server_name=config.server['name'],
            pv_name=pv,
            value=value,
            timestamp=time(),
            fallback=True
        ).model_dump()

    sio.emit('get_value', data, room=sid)

@sio.event
def put_value(sid, data):
    pv = data["pv"]
    value = data["value"]
    if verbose: print(f'Client {Client_list[sid]["sid"]} requested to put {value} to {pv}')
    if config.epics['state'].lower() == "virtual":
        pv = "VM-" + pv
    try: #This is faster than checking if the PV exists in the dictionary
        PV_list[pv].value = value
    except KeyError:
        epics.caput(pv, value)
    sio.emit('put_value', {'pv': pv, 'value': value}, room=sid)

@sio.event
def get_buffer(sid, data):
    pv = data["pv"]
    if verbose: print(f'Client {Client_list[sid]["sid"]} requested buffer of {pv}')
    if config.epics['state'].lower() == "virtual":
        pv = "VM-" + pv
    try: #This is faster than checking if the PV exists in the dictionary
        buffer, timestamps = PV_list[pv].get_buffers()
        sio.emit('get_buffer', {'pv': pv, 'buffer': buffer, 'timestamps': timestamps}, room=sid)
    except KeyError:
        sio.emit('get_buffer', {'pv': pv, 'buffer': None, 'timestamps': None}, room=sid)

@sio.event
def start_monitor(sid, data):
    pv = data["pv"]
    if verbose: print(f'Client {Client_list[sid]["sid"]} requested to start monitor of {pv}')
    length = data["length"]
    if config.epics['state'].lower() == "virtual":
        pv = "VM-" + pv
    if pv not in PV_list:
        PV_list[pv] = EI.PVInterface(pv)
        PV_list[pv].buffer_size = length
        PV_list[pv].writeAccess = True
        PV_list[pv].pv.connect()
    sio.emit("start_monitor", {'pv': pv}, room=sid)

@sio.event
def stop_monitor(sid, data):
    pv = data["pv"]
    if verbose: print(f'Client {Client_list[sid]["sid"]} requested to start monitor of {pv}')
    if config.epics['state'].lower() == "virtual":
        pv = "VM-" + pv
    if pv in PV_list:
        PV_list.pop(pv)
    sio.emit("stop_monitor", {'pv': pv}, room=sid)

@sio.event
def subscribe(sid, data):
    pv = data["pv"]
    if verbose: print(f'Client {Client_list[sid]["sid"]} requested to subscribe to {pv}')
    if config.epics['state'].lower() == "virtual":
        pv = "VM-" + pv
    if pv not in PV_list:
        PV_list[pv] = EI.PVInterface(pv)
    PV_list[pv].subscribe(sid)
    sio.emit("subscribe", {'pv': pv}, room=sid)
    
@sio.event
def unsubscribe(sid, data):
    pv = data["pv"]
    if verbose: print(f'Client {Client_list[sid]["sid"]} requested to unsubscribe to {pv}')
    if config.epics['state'].lower() == "virtual":
        pv = "VM-" + pv
    if pv in PV_list:
        PV_list[pv].unsubscribe(sid)
    sio.emit("unsubscribe", {'pv': pv}, room=sid)

@sio.event
def send_new(sid, payload):
    name = payload['name']
    value = payload['value']
    sids = payload['sids']
    for sid in sids:
        sio.emit('new_value', {'pv': name, 'value': value}, room=sid)

@sio.event
def list_monitors(sid, payload):
    if verbose: print(f'Client {Client_list[sid]["sid"]} requested list of monitors')
    monitors = list(PV_list.keys())
    sio.emit('list_monitors', {'monitors': monitors}, room=sid)

if __name__ == '__main__':
    #TODO: Log the start of the server
    start_monitors(config.epics['pv-list'])
    wsgi.server(eventlet.listen((config.server['ip'], config.server['port'])), site=app)