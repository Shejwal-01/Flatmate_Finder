from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    
    sender_id : int
    receiver_id : int
    flat_id : int
    message : str
 
    class Config:
        from_attributes = True