import pydantic as pd
from typing import TypeVar, Generic, Tuple, List

EpicsType = TypeVar('EpicsType', str, int, float, bool, bytes) #Pyepics reduces everything to these types 

class auth_out(pd.BaseModel):
    sever_name: str = 'None' #name from config file
    auth: bool #Whether or not authentication was successful
    clients: int #Number of clients connected to the server
    monitors: list #List of monitors connected to the server

class get_value_in(pd.BaseModel, Generic[EpicsType]):
    pv_name: str #Must be a valid PV name

class get_value_out(pd.BaseModel, Generic[EpicsType]):
    server_name: str = 'None' #Not mandatory
    pv_name: str #Must be a valid PV name
    value: EpicsType #Must be a valid EPICS type (str, int, float, bool or bytes)
    timestamp: float #Time of last update in seconds 
    fallback: bool #Whether or not ca fallback was used

class put_value_in(pd.BaseModel, Generic[EpicsType]):
    pv_name: str #Must be a valid PV name
    new_value: EpicsType #Must be a valid EPICS type (str, int, float, bool or bytes)

class put_value_out(pd.BaseModel, Generic[EpicsType]):
    server_name: str = 'None' #Not mandatory
    pv_name: str #Must be a valid PV name
    old_value: EpicsType #Must be a valid EPICS type (str, int, float, bool or bytes)
    new_value: EpicsType #Must be a valid EPICS type (str, int, float, bool or bytes)
    fallback: bool #Whether or not ca fallback was used

class get_buffer_in(pd.BaseModel, Generic[EpicsType]):
    pv_name: str
    length: int

class get_buffer_out(pd.BaseModel, Generic[EpicsType]):
    server_name: str = 'None' #Not mandatory
    pv_name: str #Must be a valid PV name
    buffer: List[EpicsType] #Must be a valid EPICS type (str, int, float, bool or bytes)
    timestamps: List[float] #Time of last update in seconds
    length: int #Length of the buffer

class subscribe(pd.BaseModel, Generic[EpicsType]):
    server_name: str = 'None' #Not mandatory
    pv_name: str #Must be a valid PV name


class new_value(pd.BaseModel, Generic[EpicsType]):
    server_name: str = 'None' #Not mandatory
    pv_name: str #Must be a valid PV name
    value: EpicsType #Must be a valid EPICS type (str, int, float, bool or bytes)
    timestamp: float #Time of last update in seconds


class start_monitor(pd.BaseModel, Generic[EpicsType]):
    pass

class stop_monitor(pd.BaseModel, Generic[EpicsType]):
    pass

class list_monitors(pd.BaseModel, Generic[EpicsType]):
    pass