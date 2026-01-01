from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.utils.security import hash_password, verify_password
from backend.utils.jwt import create_access_token
from backend.schemas.user import UserCreate
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from backend.dependencies.auth import get_current_user

templates = Jinja2Templates(directory="frontend/templates")


router = APIRouter(prefix = "/auth", tags = ["Authorization"])

@router.get("/register")
def show_site(request: Request, success: int | None = None):
    alert = None
    
    if success == 1:
        alert = "Registered successfully!"
    elif success == 0:
        alert = "Invalid credentials"
        
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
        return RedirectResponse(
        url="/auth/register?success=0",
        status_code=303
    )
    
    user = UserCreate(
        
        name = name,
        username = username,
        email = email,
        password = password,
        gender = gender,
        city = city
    ) 
    
    hashed_password = hash_password(user.password)
    
    new_user = User(
        
        name = user.name,
        username = user.username,
        email = user.email,
        password = hashed_password,
        gender = user.gender.value,
        city = user.city
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return RedirectResponse(
        url="/auth/register?success=1",
        status_code=303
    )


@router.get("/login")
def show_login(
    request: Request,
    
    success: int | None = None,
    logged_out: int | None = None
):
    alert = None
    alert_type = "info"

    if success == 1:
        alert = "Login successful!"
        alert_type = "success"
    elif success == 0:
        alert = "Invalid username or password"
        alert_type = "danger"
    elif logged_out == 1:
        alert = "Logged out successfully"
        alert_type = "warning"

    return templates.TemplateResponse(
        "login.html",
        {
            
            "request": request,
            "alert": alert,
            "alert_type": alert_type
        }
    )


@router.post("/login")
def login(
    request: Request,
    
    username : str = Form(...),
    password: str =Form(...),
    db: Session = Depends(get_db)
    ):
    
    user_login = (db.query(User).filter(User.username == username).first())

    if not user_login or not verify_password(password, user_login.password):
        return RedirectResponse(
        url="/auth/login?success=0",
        status_code=303)

    token = create_access_token({"user_id": user_login.id})
    
    response = RedirectResponse(
        url="/dash",
        status_code=303
    )
    response.set_cookie(key="access_token", value=token, httponly=True, samesite="lax", secure=True)

    return response
