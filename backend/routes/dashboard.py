from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from backend.models.flat import Flat
from backend.database import get_db
from fastapi.templating import Jinja2Templates
from backend.dependencies.auth import get_current_user
from backend.models.user import User
from backend.schemas.flat_post import Flat_PostCreate, GenderEnum

templates = Jinja2Templates(directory="frontend/templates")


router = APIRouter(prefix = "/dash", tags = ["Dashboard"])



@router.get("/")
def show_dashboard(request: Request, 
                   current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    posts = (
    db.query(Flat)
    .order_by(Flat.created_at.desc())
    .all()
)

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": current_user, "posts": posts}
    )
    

@router.get("/flatpost/createpost")
def create_flatpost(
    request: Request,
    success: int | None = None,
    current_user: User = Depends(get_current_user)
):
    alert = None

    if success == 1:
        alert = "Flat post created!"

    return templates.TemplateResponse(
        "flatpost.html",
        {
            "request": request,
            "user": current_user,
            "alert": alert
        }
    )

    
@router.post("/flatpost/createpost")
def create_flatpost(request: Request,
    current_user: User = Depends(get_current_user),
    location: str = Form(...),
    city : str = Form(...),
    flatmates_required: int = Form(...),
    rent: int =Form(...),
    preferred_gender: GenderEnum = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
    ):
    flat_data = Flat_PostCreate(
        
        location=location,
        city=city,
        flatmates_required=flatmates_required,
        rent=rent,
        preferred_gender=preferred_gender,
        description=description
    )
    
    new_flatpost = Flat(
        
        user_id=current_user.id,
        user_name=current_user.username,
        location=flat_data.location,
        city=flat_data.city,
        flatmates_required=flat_data.flatmates_required,
        rent=flat_data.rent,
        preferred_gender=flat_data.preferred_gender.value,  # save string
        description=flat_data.description
    )
    try:
        db.add(new_flatpost)
        db.commit()
        db.refresh(new_flatpost)
    except:
        db.rollback()
        raise
    
    return RedirectResponse(
        url="/dash/flatpost/createpost?success=1",
        status_code=303
    )
    


@router.get("/logout")
def logout_user():
    
    response = RedirectResponse("/auth/login?logged_out=1", status_code=302)
    response.delete_cookie("access_token")
    return response


@router.get("/flatpost/deletepost")
def delete_flatpost(
    request: Request,
    success: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    posts = (
    db.query(Flat)
    .order_by(Flat.created_at.desc())
    .all())
    alert = None

    if success == 1:
        alert = "Flat post deleted!"

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": current_user,
            "posts": posts,
            "alert": alert
        }
    )

@router.post("/flatpost/deletepost/{id}")
def delete_flatpost(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    flat = db.query(Flat).filter(
        Flat.id == id,
        Flat.user_id == current_user.id
    ).first()

    if not flat:
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        db.delete(flat)
        db.commit()
    
    return RedirectResponse(
    url="/dash/flatpost/deletepost?success=1",
    status_code=303)