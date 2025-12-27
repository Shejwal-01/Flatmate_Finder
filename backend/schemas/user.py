from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class UserCreate(BaseModel):
    
    username : str
    name : str
    email : EmailStr
    password : str
    gender : GenderEnum
    city : str
    created_at : datetime
    
class UserLogin(BaseModel):
    
    username : str
    password : str
    email : EmailStr
    created_at : datetime
    
    class config:
        from_attributes = True
        
        
