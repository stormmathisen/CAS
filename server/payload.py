import pydantic as pd

class auth_out(pd.BaseModel):
    sever_name: str = 'None'
    auth: bool
    clients: int
    monitors: list
