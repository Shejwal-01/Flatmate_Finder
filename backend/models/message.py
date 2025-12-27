import enum
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from backend.database import base

class message(base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key = True, index = True )
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    flat_id = Column(Integer)
    message = Column(String)
    timestamp = Column(TIMESTAMP, server_default=func.now())
    
    sender_id = Column(Integer,
        ForeignKey("users.id"))
    receiver_id = Column(Integer,
        ForeignKey("users.id"))
    flat_id = Column(Integer,
        ForeignKey("flats_id"))