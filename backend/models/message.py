from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from backend.database import base

class Message(base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key = True, index = True )
   
    message = Column(Text)
    timestamp = Column(TIMESTAMP, server_default=func.now())
    
    sender_id = Column(Integer,
        ForeignKey("users.id"))
    receiver_id = Column(Integer,
        ForeignKey("users.id"))
    flat_id = Column(Integer,
        ForeignKey("flats_id"))