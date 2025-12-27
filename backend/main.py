from fastapi import FastAPI
from backend.routes.auth import router as auth_router
from backend.routes.flats import router as flat_router
from backend.routes.messages import router as msg_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(flat_router)
app.include_router(msg_router)

@app.get("/")
def root():
    return {"message": "API is running"}