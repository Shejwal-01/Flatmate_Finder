from fastapi import FastAPI
from backend.routes.auth import router as auth_router

from backend.routes.auth import router

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "API is running"}

# @app.get("/hello")
# def hello():
#     return {"message": "Hello World"}
