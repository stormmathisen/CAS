import os
os.path.join(os.path.dirname('..\\clara\\machine'), 'static')
from pv import PVBuffer, PVArrayBuffer
import numpy as np

class PVInterface(PVBuffer):
    def __init__(self, pv_name, buffer_size=128):
        super().__init__(pv_name, buffer_size=buffer_size)
        
    @property
    def buffer_size(self):
        return self._buffer_size
    
    @buffer_size.setter
    def buffer_size(self, buffer_size):
        self.size = buffer_size
        self.resize_deque()
    
    def get_buffers(self):
        return self.buffer, self.time_buffer