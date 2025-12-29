from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.routes.auth import router as auth_router
from backend.routes.auth import templates
from backend.routes.flats import router as flat_router
from backend.routes.messages import router as msg_router
from backend.routes.dashboard import router as dash_router

app = FastAPI(title= "FlatMate Finder API", version="1.0.0")
app.include_router(auth_router)
app.include_router(flat_router)
app.include_router(msg_router)
app.include_router(dash_router)

@app.get("/")
def show_site(request: Request):
    return templates.TemplateResponse(
         "index.html",{"request": request}
    )