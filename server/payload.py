import pydantic as pd

class auth_out(pd.BaseModel):
    sever_name: str = 'None' #name from config file
    auth: bool #Whether or not authentication was successful
    clients: int #Number of clients connected to the server
    monitors: list #List of monitors connected to the server


