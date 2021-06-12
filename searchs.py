from typing import List

from main import app, get_db, manager
from sqlalchemy.orm.session import Session
from sqlalchemy import and_
from fastapi import Depends

import exceptions
import models
import schemas


@app.post("/get_users", response_model=List[schemas.UserForSearchAnswer])
def get_users(search_user: schemas.UserForSearchRequest, user: models.User = Depends(manager), db_session: Session = Depends(get_db)):
    if user.type == models.UserType.user:
        raise exceptions.PermissionDenied
    return db_session.query(models.User).filter(and_(
        models.User.first_name.like("%" + search_user.first_name + "%") if search_user.first_name is not None else True,
        models.User.last_name.like("%" + search_user.last_name + "%") if search_user.last_name is not None else True,
        models.User.email.like("%" + search_user.email + "%") if search_user.email is not None else True,
        models.User.nickname.like("%" + search_user.nickname + "%") if search_user.nickname is not None else True
    )).limit(search_user.count).offset(search_user.offset).all()


@app.post("api/v1/search_article", response_model=List[schemas.Article])
def search_article(search_props: schemas.SearchArticle, user: models.User = Depends(manager),
                   db_session: Session = Depends(get_db)):
    if search_props.status != models.ModerationStatus.published and user.type < models.UserType.moderator.value:
        raise exceptions.PermissionDenied

    return db_session.query(models.Article).filter(and_(
        models.Article.header.like('%'+search_props.header+'%'),
        models.Article.content.like('%'+search_props.content+'%'),
        models.Article.author_id.like(search_props.author_id)
    )).all()
