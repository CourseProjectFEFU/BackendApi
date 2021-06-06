from sqlalchemy.orm.session import Session
from sqlalchemy import or_
from fastapi import Depends
from fastapi.responses import JSONResponse

from main import app, get_db, manager
import schemas
import exceptions
import models


@app.post("/api/v1/ban_user", response_model=schemas.RequestResult)
def ban_user(
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
    if not db_deleting_user:
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


@app.post("/api/v1/add_moderator", response_model=schemas.RequestResult)
def add_moderator(
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
