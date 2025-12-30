from fastapi import APIRouter, Depends, Request, HTTPException, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from backend.database import get_db
from backend.dependencies.auth import get_current_user
from backend.models.message import Message
from backend.models.user import User

templates = Jinja2Templates(directory="frontend/templates")

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/{receiver_id}")
def open_chat(
    receiver_id: int,
    flat_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    receiver = db.query(User).filter(User.id == receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="User not found")

    messages = (
        db.query(Message)
        .filter(
            Message.flat_id == flat_id,
            (
                (Message.sender_id == current_user.id) &
                (Message.receiver_id == receiver_id)
            ) |
            (
                (Message.sender_id == receiver_id) &
                (Message.receiver_id == current_user.id)
            )
        )
        .order_by(Message.timestamp)
        .all()
    )

    return templates.TemplateResponse(
        "messages.html",
        {
            "request": request,
            "receiver": receiver,
            "messages": messages,
            "flat_id": flat_id,
            "current_user": current_user,
        }
    )

@router.post("/send")
def send_message(
    receiver_id: int = Form(...),
    flat_id: int = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        flat_id=flat_id,
        message=message,
    )

    db.add(new_message)
    db.commit()

    return {"success": True}
