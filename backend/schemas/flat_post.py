from pydantic import BaseModel
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    any = "any"


class Flat_PostCreate(BaseModel):
    
    location : str
    city : str
    flatmates_required : int
    rent : int
    preferred_gender : GenderEnum
    description : str
    
    class config:
        from_attributes = True
  
        