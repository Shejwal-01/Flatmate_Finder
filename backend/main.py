from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from backend.database import engine
from backend.models import Base
from backend.routes.auth import router as auth_router, templates
from backend.routes.messages import router as msg_router
from backend.routes.dashboard import router as dash_router


@asynccontextmanager
async def lifespan(app: FastAPI):
   
    Base.metadata.create_all(bind=engine)
    yield



app = FastAPI(
    title="FlatMate Finder API",
    version="1.0.0",
    lifespan=lifespan
)

# Routers
app.include_router(auth_router)
app.include_router(msg_router)
app.include_router(dash_router)

# Static files
app.mount(
    "/frontend/static",
    StaticFiles(directory="frontend/static"),
    name="static",
)

@app.get("/")
def show_site(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
