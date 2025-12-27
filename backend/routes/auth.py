from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.utils.security import hash_password, verify_password
from backend.utils.jwt import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="frontend/templates")


router = APIRouter(prefix = "/auth", tags = ["Authorization"])

@router.get("/register")
def show_site(request: Request, success: int = 0):
    alert = None
    if success:
        alert = "Registration successful! Login" 
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "alert": alert}
    )



@router.post("/register")
def register(
    request: Request,
    name: str = Form(...),
    username : str = Form(...),
    email: str = Form(...),
    password: str =Form(...),
    gender: str = Form(...),
    city: str = Form(...),
    db: Session = Depends(get_db)
    ):
    
    existing_byemail = db.query(User).filter(User.email == email).first()
    existing_byusername = db.query(User).filter(User.username == username).first()
    if existing_byemail or existing_byusername:
        raise HTTPException(status_code=400, detail="User already registered")
    
    new_user = User(
        
        name = name,
        username = username,
        email = email,
        password = hash_password(password),
        gender = gender,
        city = city
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return RedirectResponse(
        url="/auth/register?success=1",
        status_code=303
    )


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
