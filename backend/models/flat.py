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
    location = Column(String(200), nullable = False)
    city = Column(String(100), nullable = False)
    rent = Column(Integer, nullable = False)
    flatmates_required = Column(Integer, nullable = False)
    preferred_gender = Column(Enum(GenderEnum), nullable = False)
    description = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    user_id = Column(Integer,
        ForeignKey("users.id", ondelete="CASCADE"))