from pydantic import BaseModel, EmailStr, text
from datetime import datetime
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    any = "any"


class Flat_PostCreate(BaseModel):
    
    username : str
    location : str
    city : str
    flatmates_required : int
    rent : int
    preferred_gender : GenderEnum
    description : text
    created_at : datetime
    
class UserResponse(BaseModel):
    
    id : int
    user_id : int
    username : str
    location : str
    city : str
    rent : int
    flatmates_required : int
    created_at : datetime
    
    class config:
        from_attributes = True
        