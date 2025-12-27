from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    
    receiver_id : int
    flat_id : int
    message : str
 
    class config:
        from_attributes = True