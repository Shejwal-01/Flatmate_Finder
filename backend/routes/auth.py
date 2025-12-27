from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.schemas.user import UserCreate, UserLogin
from backend.utils.security import hash_password, verify_password
from backend.utils.jwt import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix = "/auth", tags = ["Authorization"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        
        name = user.name,
        username = user.username,
        email = user.email,
        password = hash_password(user.password),
        gender = user.gender,
        city = user.city,
        created_at = user.created_at
        
    )
    
    db.add(new_user)
    db.commit()
    
    return {"message": "User registered successfully"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(get_db)):
    
    user_login = (db.query(User).filter(User.username == form_data.username).first())

    if not user_login or not verify_password(form_data.password, user_login.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user_login.id})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
