import eventlet
from eventlet import wsgi
import socketio

virtual = True
verbose = True

if virtual:
    import os
    os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.246"
    os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
    os.environ["EPICS_CA_SERVER_PORT"] = "6020"
    import epics
else:
    import epics

def check_auth(client_id, secret):
    return True

PV_list = {}
Buffer_list = {}
Client_list = {}

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ, auth):
    new_client = {}
    new_client['sid'] = sid
    new_client['ip'] = environ['REMOTE_ADDR']
    if check_auth(sid, auth):
        new_client['auth'] = auth
        Client_list[sid] = new_client
        sio.emit('auth_success', room=sid)
    else:
        sio.emit('auth_fail', room=sid)
    if verbose: print(f'Client {Client_list[sid]} connected from {sid}')
    #TODO: Log the connection

if __name__ == '__main__':
    wsgi.server(eventlet.listen(('', 5000)), site=app)
