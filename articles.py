from sqlalchemy.orm.session import Session
from sqlalchemy import or_
from fastapi import Depends
from fastapi.responses import JSONResponse
from datetime import datetime

from typing import List

from main import app, get_db, manager
import schemas
import exceptions
import models


@app.post("/api/v1/add_article", response_model=schemas.RequestResult)
def add_article(
    article_model: schemas.ArticleForAdd,
    categories_list: List[int],
    db_session: Session = Depends(get_db),
    user: models.User = Depends(manager),
):
    article = models.Article()
    article.header = article_model.header
    article.content = article_model.content
    article.author_id = user.id
    if user.type.value >= models.UserType.moderator.value:
        article.status = models.ModerationStatus.published
        article.publication_date = datetime.now()
    db_session.add(article)
    db_session.commit()
    db_session.flush()
    return {"result": "success"}


@app.post("/api/v1/change_article/{article_id}", response_model=schemas.RequestResult)
def change_the_article(
    changing_props: schemas.Article,
    article_id: int,
    user: models.User = Depends(manager),
    db_session: Session = Depends(get_db),
):
    if user.type.value < models.UserType.moderator.value:
        raise exceptions.PermissionDenied

    article = (
        db_session.query(models.Article)
        .filter(models.Article.id == article_id)
        .one_or_none()
    )
    if article is None:
        raise exceptions.ArticleDoesNotExists

    for i in changing_props.__fields_set__:
        if i == "status":
            article.status = models.ModerationStatus(changing_props[i])
        else:
            setattr(article, i, changing_props[i])

    db_session.commit()
    db_session.flush()

    return {"result": "success"}

