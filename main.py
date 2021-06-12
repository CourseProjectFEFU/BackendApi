import secrets
import models
import uvicorn

from sqlalchemy.orm.session import Session

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from fastapi_login import LoginManager

from db import SessionLocal, engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
SECRET = "5c4b93fc508656a184874da6dd27a8db74b1dcf8db2d489be4afbc36499b312737c1c7228b6a2e0469ac9645d24dbabdda3feb49e00c6\
f14b0bad7e4b1faab16debcab276930365faa28d2127bcc7bb974869fe371a9b6b2d082e97321fcc17a799d577a4c1856e29aa8783f3a3d2d25a0f2\
04493628c9f2a87bda24b7bbb5cd"
manager = LoginManager(SECRET, "/api/v1/login", use_cookie=True)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "https://course-project-front.herokuapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Access-Control-Expose-Headers
    expose_headers=["set-cookie"],
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import exceptions
import auth
import userTypeChange
import articles
import searchs


@app.get("/")
async def hello_world():
    return {"Hello": "World"}
