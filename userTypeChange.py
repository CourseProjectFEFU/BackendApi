from sqlalchemy.orm.session import Session
from sqlalchemy import or_
from fastapi import Depends
from fastapi.responses import JSONResponse

from main import app, get_db, manager
import schemas
import exceptions
import models


@app.post("/api/v1/ban_user", response_model=schemas.RequestResult, tags=["User data manipulation"])
async def ban_user(
    deleting_user: schemas.ChangingTypeUser,
    user: models.User = Depends(manager),
    db_session: Session = Depends(get_db),
):
    db_deleting_user: models.User = (
        db_session.query(models.User)
        .filter(
            or_(
                models.User.email == deleting_user.identifier,
                models.User.nickname == deleting_user.identifier,
            )
        )
        .one_or_none()
    )
    if db_deleting_user is None:
        raise exceptions.UserDoesNotExists
    if db_deleting_user.type.value >= user.type.value:
        return JSONResponse(
            status_code=403,
            content={
                "result": "error",
                "error_description": "Unauthorized for this action",
            },
        )
    db_deleting_user.type = models.UserType.banned
    db_session.commit()
    db_session.flush()

    return JSONResponse(status_code=200, content={"result": "success"})


@app.post("/api/v1/add_moderator", response_model=schemas.RequestResult, tags=["User data manipulation"])
async def add_moderator(
    adding_user: schemas.ChangingTypeUser,
    user: models.User = Depends(manager),
    db_session: Session = Depends(get_db),
):
    if user.type != models.UserType.administrator:
        raise exceptions.PermissionDenied

    db_adding_user: models.User = (
        db_session.query(models.User).filter(
            or_(
                models.User.email == adding_user.identifier,
                models.User.nickname == adding_user.identifier,
            )
        )
    ).one_or_none()

    if db_adding_user is None:
        raise exceptions.UserDoesNotExists

    db_adding_user.type = models.UserType.moderator
    db_session.commit()
    db_session.flush()

    return JSONResponse(status_code=200, content={"result": "success"})


@app.post("/api/v1/unban_user", response_model=schemas.RequestResult, tags=["User data manipulation"])
async def unban_user(
    unbaning_user: schemas.ChangingTypeUser,
    user: models.User = Depends(manager),
    db_session: Session = Depends(get_db),
):
    if user.type.value < models.UserType.moderator.value:
        raise exceptions.PermissionDenied

    db_user = (
        db_session.query(models.User)
        .filter(
            or_(
                models.User.email == unbaning_user.identifier,
                models.User.nickname == unbaning_user.identifier,
            )
        )
        .one_or_none()
    )

    if db_user is None:
        raise exceptions.UserDoesNotExists

    db_user.type = models.UserType.user
    db_session.commit()
    db_session.flush()

    return JSONResponse(status_code=200, content={"result": "success"})


@app.post("/api/v1/remove_moderator", response_model=schemas.RequestResult, tags=["User data manipulation"])
async def remove_moderator(
    removing_user: schemas.ChangingTypeUser,
    user: models.User = Depends(manager),
    db_session: Session = Depends(get_db)
):
    if user.type.value < models.UserType.administrator.value:
        raise exceptions.PermissionDenied
    user_from_db = db_session.query(models.User).filter(
        or_(
            models.User.email == removing_user.identifier,
            models.User.nickname == removing_user.identifier,
        )
    ).one_or_none()
    if user_from_db is None:
        raise exceptions.UnexpectedError
    user_from_db.type = models.UserType.user
    db_session.commit()
    db_session.flush()
    return {"result":"success"}