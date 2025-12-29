import enum
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from backend.database import base


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    any = "any"
    
class Flat(base):
    __tablename__ = "flats"
    
    id = Column(Integer, primary_key = True, index = True )
    location = Column(String(200), nullable = True)
    city = Column(String(100), nullable = True)
    rent = Column(Integer, nullable = True)
    flatmates_required = Column(Integer, nullable = True)
    preferred_gender = Column(Enum(GenderEnum), nullable = True)
    description = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    user_name = Column(String, nullable = True)
    
    user_id = Column(Integer,
        ForeignKey("users.id", ondelete="CASCADE"))