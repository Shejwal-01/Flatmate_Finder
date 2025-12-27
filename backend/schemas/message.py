from pydantic import BaseModel, text
from datetime import datetime

class MessageCreate(BaseModel):
    
    receiver_id : int
    message : text
    
class MessageResponse(BaseModel):
    
    id : int
    sender_id : int
    receiver_id : int
    message : text
    timestamp : datetime
    
    class config:
        from_attributes = True