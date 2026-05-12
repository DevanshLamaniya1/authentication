from fastapi import FastAPI
from app.db.db import Base,engine
from app.routes.user_auth import user_authentication

app = FastAPI(title="AI APP")

app.include_router(user_authentication)

Base.metadata.create_all(bind = engine)

@app.get("/")
def greet():
    return "welcome"