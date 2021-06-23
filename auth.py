import os
import hashlib
import models
from datetime import timedelta

from fastapi import Depends
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

import sqlalchemy.exc as sqlalchemyexceptions
from sqlalchemy.orm.session import Session
from sqlalchemy import or_

from main import app, manager, get_db
import exceptions
import schemas
import secrets
from mailer_functions import send_verification_link


def hash_password(password: str, salt: bytes = os.urandom(32)) -> (bytes, bytes):
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 10000)
    return key, salt


def verify_password(plain_password: str, password_salt: bytes, password_hash: bytes):
    return password_hash == hash_password(plain_password, password_salt)[0]


@manager.user_loader
async def get_user(identifier: str):
    db: Session = next(get_db())
    return (
        db.query(models.User)
            .filter(
            or_(models.User.email == identifier, models.User.nickname == identifier)
        )
            .one_or_none()
    )


@app.post("/api/v1/login", response_model=schemas.LoginResult, tags=["auth/register"])
async def login(response: JSONResponse, data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user: models.User = await get_user(email)
    if not user:
        raise InvalidCredentialsException
    elif not verify_password(password, user.salt, user.password):
        raise InvalidCredentialsException
    elif user.type == models.UserType.banned:
        raise exceptions.UserIsBanned
    elif not user.verified:
        raise exceptions.UserAccountIsNotVerified

    access_token = manager.create_access_token(
        data={"sub": user.email, "rol": user.type.value}, expires=timedelta(hours=12)
    )

    response = JSONResponse(
        status_code=200,
        content={"result": "success", "id": user.id, "username": user.nickname},
    )
    response.set_cookie(
        "access-token", value=access_token, httponly=True, samesite="none", secure=True
    )
    # manager.set_cookie(response, access_token)
    return response


@app.post("/api/v1/register", response_model=schemas.RequestResult, tags=["auth/register"])
async def new_user_register(
        user: schemas.CreateUser, db_session: Session = Depends(get_db)
):
    db_user = await get_user(user.email)
    print(db_user)
    if not db_user:
        db_user = await get_user(user.nickname)
        print(db_user)
    else:
        raise exceptions.EmailAlreadyExists
    print(db_user)
    if db_user:
        raise exceptions.NicknameAlreadyExists

    user = dict(user)
    user["password"], user["salt"] = hash_password(user["password"])
    user["verification_link_suffix"] = secrets.token_hex(30)
    db_user = models.User(**user)
    try:
        db_session.add(db_user)
        db_session.commit()
        db_session.flush()
        print(
            send_verification_link(
                f"https://news.asap-it.tech/verify/{user['verification_link_suffix']}",
                user["email"], user["first_name"] + " " + user["last_name"]
            )
        )
    except sqlalchemyexceptions.SQLAlchemyError as inst:
        print(inst)
        return JSONResponse(
            status_code=500,
            content={"result": "error", "error_description": "server_error"},
        )
    return JSONResponse(status_code=200, content={"result": "success"})


@app.post("/api/v1/update_cookie", tags=["auth/register"])
async def update_cookie(response: JSONResponse, user: models.User = Depends(manager), tags=["auth/register"]):
    access_token = manager.create_access_token(
        data={"sub": user.email, "rol": user.type.value}
    )
    if user.type == models.UserType.banned:
        raise exceptions.PermissionDenied

    response = JSONResponse(
        status_code=200,
        content={"result": "success", "id": user.id, "username": user.nickname},
    )
    # manager.set_cookie(response, access_token)
    response.set_cookie(
        "access-token", value=access_token, httponly=True, samesite="none", secure=True
    )
    return response


@app.get("/api/v1/logout", response_model=schemas.RequestResult, tags=["auth/register"])
async def logout(response: JSONResponse, user: models.User = Depends(manager)):
    response = JSONResponse(
        status_code=200,
        content={"result": "success", "success_description": "Logged out successfully"},
    )
    # manager.set_cookie(response, "")
    response.set_cookie(
        "access-token", value="", httponly=True, samesite="none", secure=True
    )
    return response


@app.post("/api/v1/change_user_data", response_model=schemas.RequestResult, tags=["User data manipulation"])
async def change_user_data(
        new_user_data: schemas.User,
        user: models.User = Depends(manager),
        db_session: Session = Depends(get_db),
):
    user_from_db = (
        db_session.query(models.User).filter(models.User.id == user.id).one_or_none()
    )
    if user_from_db is None:
        raise exceptions.UnexpectedError
    user_from_db.last_name = new_user_data.last_name
    user_from_db.first_name = new_user_data.first_name
    user_from_db.subscribed = new_user_data.subscribed
    db_session.commit()
    return {"result": "success"}


@app.get(
    "/api/v1/verify_account/{verification_link_suffix}",
    response_model=schemas.RequestResult,
    tags=["User data manipulation"]

)
async def verify_account(
        verification_link_suffix: str, db_session: Session = Depends(get_db)
):
    user = (
        db_session.query(models.User)
            .filter(
            models.User.verified == False,
            models.User.verification_link_suffix == verification_link_suffix,
        )
            .one_or_none()
    )
    if not user:
        return JSONResponse(
            status_code=400,
            content={
                "result": "error",
                "error_description": "No such user, or account is already verified",
            },
        )

    user.verified = True
    db_session.commit()

    return JSONResponse(status_code=200, content={"result": "success"})
