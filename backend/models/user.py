import enum 
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from backend.database import base

class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    
class User(base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True, index = True )
    name = Column(String(100), nullable = False)
    username = Column(String(50), nullable = False, unique = True)
    email = Column(String(100), nullable = False, unique = True)
    password = Column(String(500), nullable = False)
    
    gender = Column(Enum(GenderEnum), nullable = False)
    
    city = Column(String(100), nullable = False)
    
    created_at = Column(TIMESTAMP, server_default=func.now())