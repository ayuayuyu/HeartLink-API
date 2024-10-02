from pydantic import BaseModel


class Datas(BaseModel):
    heartRate: str
    id: str
    
class Reset(BaseModel):
    value: str
    
class Device(BaseModel):
    id: str