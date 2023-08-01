import os
import sys
sys.path.append('./lib/machine')
from pv import PVBuffer, PVArrayBuffer
import numpy as np

class PVInterface(PVBuffer):
    def __init__(self, pv_name, buffer_size=128):
        super().__init__(pv_name, maxlen=buffer_size)
        
    @property
    def buffer_size(self):
        return self.maxlen
    
    @buffer_size.setter
    def buffer_size(self, buffer_size):
        self.size = buffer_size
        self.resize_deque()
    
    def get_buffers(self):
        return list(self.buffer), list(self.timeBuffer)