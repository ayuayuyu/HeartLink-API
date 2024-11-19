from pydantic import BaseModel


class Datas(BaseModel):
    heartRate: str
    player: str
    
class Reset(BaseModel):
    value: str
    
class Device(BaseModel):
    id: str
    
class Status(BaseModel):
    status: str
    
class PlayerName(BaseModel):
    player: str
    name: str
    
class Players(BaseModel):
    player: str
    id: int
    index: int
    
    
class Names(BaseModel):
    player: str
    name: str
    
class Array(BaseModel):
    index : int
    array1 : list[str]
    array2 : list[str]
    
class indexTopics(BaseModel):
    index: int
    player: str