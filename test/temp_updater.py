import numpy as np
from time import perf_counter_ns
import os
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.246"
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_SERVER_PORT"] = "6020"
import epics

def generate_value():
    return np.random.rand(1)[0]*2-1

PVS = [
    "VM-CLA-C2V-DIA-BPM-01:X"
]

while True:
    start = perf_counter_ns()
    for PV in PVS:
        epics.caput(PV, generate_value())
    while perf_counter_ns() - start < 0.1*1e9:
        pass