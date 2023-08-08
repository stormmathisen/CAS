import os
import sys
sys.path.append('./lib/machine/')
from pv import PVBuffer, PVArrayBuffer
import numpy as np

class PVInterface(PVBuffer):
    def __init__(self, pv_name, buffer_size=128, sio=None, **kwargs):
        self.sio = sio
        self.subscription_list = []
        super().__init__(pv_name, maxlen=buffer_size)

    def callback(self, **kwargs):
        super().callback(**kwargs)
        self.new_fun(self.subscription_list, self.name, self.value)
    @property
    def buffer_size(self):
        return self.maxlen

    @buffer_size.setter
    def buffer_size(self, buffer_size):
        self.size = buffer_size
        self.resize_deque()
    
    def subscribe(self, sid):
        if sid not in self.subscription_list:
            self.subscription_list.append(sid)
    
    def unsubscribe(self, sid):
        if sid in self.subscription_list:
            self.subscription_list.remove(sid)
    
    def get_buffers(self):
        return list(self.buffer), list(self.timeBuffer)