from fastapi import APIRouter, Depends
from backend.schemas.flat_post import Flat_PostCreate
from backend.database import get_db
from sqlalchemy.orm import Session
from backend.dependencies.auth import get_current_user
from backend.models.flat import Flat
from backend.models.user import User



router = APIRouter(prefix = "/flats", tags = ["Flats"])

@router.post("/")
def create_flatpost(flat: Flat_PostCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)
                    ):
    
    new_flat_post = Flat(
        
        user_id = current_user.id,
        location =flat.location,
        city =flat.city,
        flatmates_required =flat.flatmates_required,
        rent =flat.rent,
        preferred_gender =flat.preferred_gender,
        description =flat.description
    )
    
    db.add(new_flat_post)
    db.commit()
    db.refresh(new_flat_post)
    return {
    "message": "Flat Post added successfully",
    "data": new_flat_post
    }

    
    