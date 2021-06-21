from typing import List

from main import app, get_db, manager
from sqlalchemy.orm.session import Session
from sqlalchemy import and_, desc
from fastapi import Depends

import exceptions
import models
import schemas
import hashlib


@app.post("/api/v1/get_users", response_model=List[schemas.UserForSearchAnswer])
async def get_users(
    search_user: schemas.UserForSearchRequest,
    user: models.User = Depends(manager),
    db_session: Session = Depends(get_db),
):
    if user.type == models.UserType.user:
        raise exceptions.PermissionDenied
    users: List[models.User] = (
        db_session.query(models.User)
        .filter(
            and_(
                models.User.first_name.like("%" + search_user.first_name + "%")
                if search_user.first_name is not None
                else True,
                models.User.last_name.like("%" + search_user.last_name + "%")
                if search_user.last_name is not None
                else True,
                models.User.email.like("%" + search_user.email + "%")
                if search_user.email is not None
                else True,
                models.User.nickname.like("%" + search_user.nickname + "%")
                if search_user.nickname is not None
                else True,
            )
        )
        .limit(search_user.count)
        .offset(search_user.offset)
        .all()
    )
    for user in users:
        if user.account_image is None:
            user.account_image = (
                "https://www.gravatar.com/avatar/"
                + hashlib.md5(user.email.encode("utf-8")).hexdigest()
                + "?d=retro"
            )
    db_session.commit()
    db_session.flush()
    return users


@app.post("/api/v1/search_articles_ordianry", response_model=List[schemas.Article])
async def search_article_ordinary(
    search_props: schemas.SearchArticle, db_session: Session = Depends(get_db)
):
    # if search_props.status != models.ModerationStatus.published:
    #     raise exceptions.PermissionDenied

    return (
        db_session.query(models.Article)
        .filter(
            and_(
                models.Article.header.like("%" + search_props.header + "%"),
                models.Article.content.like("%" + search_props.content + "%"),
                (models.Article.author_id == search_props.author_id)
                if search_props.author_id
                else True,
                (models.Article.id == search_props.id) if search_props.id else True,
            )
        )
        .order_by(desc(models.Article.publication_date))
        .all()
    )


@app.post("/api/v1/search_articles_moderation", response_model=List[schemas.Article])
async def search_articles_moderation(
    search_props: schemas.SearchArticle,
    user: models.User = Depends(manager),
    db_session: Session = Depends(get_db),
):
    if user.type.value < models.UserType.moderator.value:
        raise exceptions.PermissionDenied

    return (
        db_session.query(models.Article)
        .filter(
            and_(
                models.Article.header.like("%" + search_props.header + "%"),
                models.Article.content.like("%" + search_props.content + "%"),
                models.Article.author_id.like(search_props.author_id),
                models.Article.id.like(search_props.id) if search_props.id else True,
            )
        )
        .order_by(desc(models.Article.creation_date))
        .all()
    )


@app.get("/api/v1/get_self_info", response_model=schemas.SelfInfoAnswer)
async def get_self_info(user: models.User = Depends(manager)):
    return user
