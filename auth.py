import os
import hashlib
import models

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

import sqlalchemy.exc as sqlalchemyexceptions
from sqlalchemy.orm.session import Session
from sqlalchemy import or_

from main import app, manager, get_db
import exceptions
import schemas


def hash_password(password: str, salt: bytes = os.urandom(32)) -> (bytes, bytes):
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 10000)
    return key, salt


def verify_password(plain_password: str, password_salt: bytes, password_hash: bytes):
    return password_hash == hash_password(plain_password, password_salt)[0]


@manager.user_loader
def get_user_by_email(identifier: str):
    db = next(get_db())
    return (
        db.query(models.User)
        .filter(
            or_(models.User.email == identifier, models.User.nickname == identifier)
        )
        .one_or_none()
    )


def get_user_by_nickname(nickname: str):
    db = next(get_db())
    return db.query(models.User).filter_by(nickname=nickname).one_or_none()


@app.post("/api/v1/login")
def login(response: JSONResponse, data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user: models.User = get_user_by_email(email)
    if not user:
        raise InvalidCredentialsException
    elif not verify_password(password, user.salt, user.password):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={"sub": user.email, "rol": user.type.value}
    )
    response = JSONResponse(status_code=200)
    manager.set_cookie(response, access_token)
    return response


@app.post("/api/v1/register", response_model=schemas.RequestResult)
def new_user_register(user: schemas.CreateUser, db_session: Session = Depends(get_db)):
    db_user = get_user_by_email(user.email)
    if not db_user:
        db_user = get_user_by_nickname(user.nickname)
    else:
        raise exceptions.EmailAlreadyExists
    if db_user:
        raise exceptions.NicknameAlreadyExists

    user = dict(user)
    user["password"], user["salt"] = hash_password(user["password"])
    db_user = models.User(**user)
    try:
        db_session.add(db_user)
        db_session.commit()
        db_session.flush()
    except sqlalchemyexceptions.SQLAlchemyError as inst:
        print(inst)
        return JSONResponse(
            status_code=500,
            content={"result": "error", "error_description": "server_error"},
        )
    return JSONResponse(status_code=200, content={"result": "success"})
