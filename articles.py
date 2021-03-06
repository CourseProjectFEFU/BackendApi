from sqlalchemy.orm.session import Session
from sqlalchemy import desc
from fastapi import Depends
from datetime import datetime

from typing import List, Tuple

from main import app, get_db, manager
import schemas
import exceptions
import models
from mailer_functions import send_briefs


@app.post(
    "/api/v1/add_article",
    response_model=schemas.RequestResult,
    tags=["Article manipulation"],
)
async def add_article(
    article_model: schemas.ArticleForAdd,
    categories_list: List[int],
    db_session: Session = Depends(get_db),
    user: models.User = Depends(manager),
):
    article = models.Article()
    article.header = article_model.header
    article.content = article_model.content
    article.author_id = user.id
    article.image = article_model.image
    if user.type.value >= models.UserType.moderator.value:
        article.status = models.ModerationStatus.published
        article.publication_date = datetime.now()
    db_session.add(article)
    article_id = article.id
    for cat_id in categories_list:
        category = (
            db_session.query(models.Category)
            .filter(models.Category.id == cat_id)
            .one_or_none()
        )
        if category is None:
            raise exceptions.InvalidCategory
        db_session.add(
            models.article_category_association_table(
                article_id=article_id, category_id=cat_id
            )
        )
    db_session.commit()
    db_session.flush()
    return {"result": "success"}


@app.post(
    "/api/v1/change_article/{article_id}",
    response_model=schemas.RequestResult,
    tags=["Article manipulation"],
)
async def change_the_article(
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

    # for i in changing_props.__fields_set__:
    #     if i == "status":
    #         article.status = models.ModerationStatus(changing_props[i])
    #         if changing_props[i] == models.ModerationStatus.published.value:
    #             article.publication_date = datetime.now()
    #     else:
    #         setattr(article, i, changing_props[i])
    article.image = changing_props.image
    article.header = changing_props.header
    article.content = changing_props.content
    article.status = changing_props.status
    if changing_props.status.value == models.ModerationStatus.published.value:
        article.publication_date = datetime.now()

    db_session.commit()
    db_session.flush()

    return {"result": "success"}


@app.get(
    "/api/v1/send_briefs",
    response_model=schemas.RequestResult,
    tags=["Article manipulation"],
)
async def send_briefs_to_subscribed_users(
    user: models.User = Depends(manager), db_session: Session = Depends(get_db)
):
    if user.type.value < models.UserType.moderator.value:
        raise exceptions.PermissionDenied
    users_for_sending = (
        db_session.query(models.User).filter(models.User.subscribed).all()
    )
    if len(users_for_sending) == 0:
        return {"result": "success"}
    emails_for_sending: List[Tuple[str, str]] = [
        (user.email, user.first_name + " " + user.last_name)
        for user in users_for_sending
    ]
    articles = (
        db_session.query(models.Article)
        .filter(models.Article.status == models.ModerationStatus.published)
        .order_by(desc(models.Article.publication_date))
        .limit(10)
        .offset(0)
        .all()
    )
    text = "Check our new exciting news\n"
    for article in articles:
        text += f'<a href="https://news.asap-it.tech/new/{article.id}">{article.header}</a><br/>'
    send_briefs(emails_for_sending, text)
    return {"result": "success"}
