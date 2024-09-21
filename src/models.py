from pydantic import BaseModel


class Datas(BaseModel):
    heartRate: str
    
class Reset(BaseModel):
    value: str