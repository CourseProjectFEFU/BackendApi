import secrets
import models
import uvicorn

from sqlalchemy.orm.session import Session

from fastapi import FastAPI, Depends

from fastapi_login import LoginManager

from db import SessionLocal, engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
SECRET = secrets.token_hex(128)
manager = LoginManager(SECRET, "/api/v1/login", use_cookie=True)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import exceptions
import auth

@app.get("/hello_world")
def hello_world(user=Depends(manager)):
    return {"hello": "world"}

