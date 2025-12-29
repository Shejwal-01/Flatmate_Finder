from pydantic import BaseModel, EmailStr
from datetime import datetime
from backend.models.user import GenderEnum


class UserCreate(BaseModel):
    
    username : str
    name : str
    email : EmailStr
    password : str
    gender : GenderEnum
    city : str
    created_at : datetime
    
    class config:
        from_attributes = True
        
        
