from enum import Enum
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

base = declarative_base()

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    any = "any"
    
class flat(base):
    __tablename__ = "flats"
    
    id = Column(Integer, primary_key = True, index = True )
    user_id = Column(Integer)
    location = Column(String(200))
    city = Column(String(100))
    rent = Column(Integer)
    flatmates_required = Column(Integer)
    preferred_gender = Column(GenderEnum)
    description = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    user_id = Column(Integer,
        ForeignKey("users.id", ondelete="CASCADE"))