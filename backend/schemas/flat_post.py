from pydantic import BaseModel
from backend.models.flat import GenderEnum



class Flat_PostCreate(BaseModel):
    
    location : str
    city : str
    flatmates_required : int
    rent : int
    preferred_gender : GenderEnum
    description : str
    
    class Config:
        from_attributes = True
  
        