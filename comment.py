from sqlalchemy.orm.session import Session
from sqlalchemy import or_, and_, desc
from fastapi import Depends
from fastapi.responses import JSONResponse
from datetime import datetime

from typing import List

from main import app, get_db, manager

import schemas
import exceptions
import models


@app.post(
    "/api/v1/add_comment",
    response_model=schemas.Comment,
    tags=["Comments manipulation"],
)
async def add_comment(
    comment: schemas.AddComment,
    user: models.User = Depends(manager),
    db_session: Session = Depends(get_db),
):
    comment_model = models.Comment()
    comment_model.content = comment.content
    comment_model.author_id = user.id
    comment_model.article_id = comment.article_id
    comment_model.reply_id = comment.reply_id
    db_session.add(comment_model)
    db_session.commit()
    db_session.flush()

    return comment;


@app.post(
    "/api/v1/get_article_comments/{article_id}",
    response_model=List[schemas.Comment],
    tags=["Comments manipulation"],
)
async def get_article_comments(article_id: int, db_session: Session = Depends(get_db)):
    article = (
        db_session.query(models.Article)
        .filter(models.ArticleWithComments.id == article_id)
        .one_or_none()
    )
    if not article:
        raise exceptions.ArticleDoesNotExists
    comments = (
        db_session.query(models.CommentWithAuthor)
        .with_parent(article, models.ArticleWithComments.comments)
        .filter(
            and_(
                models.CommentWithAuthor.reply_id == None,
                models.CommentWithAuthor.status == models.ModerationStatus.published,
            )
        )
        .order_by(desc(models.Comment.creation_date))
        .all()
    )
    return comments


@app.post(
    "/api/v1/get_comments_for_moderation",
    response_model=List[schemas.Comment],
    tags=["Comments manipulation"],
    deprecated=True,
)
async def get_comments_for_moderation(
    user: models.User = Depends(manager), db_session: Session = Depends(get_db)
):
    if user.type.value < models.UserType.moderator.value:
        raise exceptions.PermissionDenied
    comments = (
        db_session.query(models.Comment)
        .filter(models.Comment.status == models.ModerationStatus.waiting)
        .order_by(desc(models.Comments.creation_date))
        .all()
    )
    return comments


@app.post(
    "/api/v1/change_comment_status/{comment_id}/{status}",
    response_model=schemas.RequestResult,
    tags=["Comments manipulation"],
)
async def change_comment_status(
    comment_id: int,
    status: int,
    user: models.User = Depends(manager),
    db_session: Session = Depends(get_db),
):
    if user.type.value < models.UserType.moderator.value:
        raise exceptions.PermissionDenied

    comment = (
        db_session.query(models.Comment)
        .filter(models.Comment.id == comment_id)
        .one_or_none()
    )
    if comment is None:
        raise exceptions.CommentDoesNotExists

    comment.status = models.ModerationStatus(status)

    db_session.commit()
    db_session.flush()

    return {"result": "success"}
