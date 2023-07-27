from epics import PV
import numpy as np

class PV_Buffer(object):
    def __init__(self, pv_name, buffer_size=128):
        self.PV = PV(pv_name, form='time')
        self.PV.connect()
        self.buffer = np.zeros((buffer_size, self.PV.nelm))
        self.timestamps = np.zeros((buffer_size, 2), dtype=np.int64)
        self.index = None
    
    def callback_fn(self, pvname=None, value=0.0, timestamp=0.0, **kw):
        self.update_buffer(value, timestamp)
    
    def start(self):
        self.index = self.PV.add_callback(self.callback_fn)
    
    def stop(self):
        self.PV.remove_callback(self.index)
        self.index = None
    
    def get_buffer(self):
        return self.buffer.tolist(), self.timestamps.tolist()
    
    def update_buffer(self, value, timestamp):
        self.buffer = np.roll(self.buffer, -1, axis=0)
        self.timestamps = np.roll(self.timestamps, -1, axis=0)
        self.buffer[-1,:] = value
        self.timestamps[-1,0] = int(timestamp)
        self.timestamps[-1,1] = int((timestamp - int(timestamp))*1e9)