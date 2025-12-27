from fastapi import APIRouter, Depends, HTTPException
from backend.schemas.message import MessageCreate
from backend.database import get_db
from sqlalchemy.orm import Session
from backend.dependencies.auth import get_current_user
from backend.models.message import Message
from backend.models.user import User

router = APIRouter(prefix= "/messages", tags = ["Messages"])

@router.post("/")
def send_message(msg: MessageCreate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)
                 ):
    
    new_message = Message(
        
        sender_id = current_user.id,
        receiver_id = msg.receiver_id,
        flat_id = msg.flat_id,
        message = msg.message
    )
    
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {
        "data": new_message
        }