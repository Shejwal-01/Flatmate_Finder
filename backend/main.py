from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.routes.auth import router as auth_router
from backend.routes.auth import templates
from backend.routes.messages import router as msg_router
from backend.routes.dashboard import router as dash_router
from fastapi.staticfiles import StaticFiles
from backend.models import Base
from backend.database import engine



app = FastAPI(title= "FlatMate Finder API", version="1.0.0")
app.include_router(auth_router)
app.include_router(msg_router)
app.include_router(dash_router)

app.mount(
    "/frontend/static",
    StaticFiles(directory="frontend/static"),
    name="static",
)
Base.metadata.create_all(bind=engine)
@app.get("/")
def show_site(request: Request):
    return templates.TemplateResponse(
         "index.html",{"request": request}
    )