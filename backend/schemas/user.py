from pydantic import BaseModel, EmailStr
from datetime import datetime
from backend.models.user import GenderEnum
from backend.utils.security import hash_password

class UserCreate(BaseModel):
    
    username : str
    name : str
    email : EmailStr
    password :str
    gender : GenderEnum
    city : str
    
    class Config:
        from_attributes = True
        
        
