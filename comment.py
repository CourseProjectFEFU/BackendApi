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


@app.post("/api/v1/add_comment", response_model=schemas.RequestResult)
async def add_comment(comment: schemas.AddComment,
                      user: models.User = Depends(manager),
                      db_session: Session = Depends(get_db)):
    comment_model = models.Comment()
    comment_model.content = comment.content
    comment_model.author_id = user.id
    comment_model.article_id = comment.article_id
    comment_model.reply_id = comment.reply_id
    db_session.add(comment_model)
    db_session.commit()
    db_session.flush()

    return {"result": "success"}


@app.post("/api/v1/get_article_comments/{article_id}", response_model=List[schemas.Comment])
async def get_article_comments(article_id: int, db_session: Session = Depends(get_db)):
    article = db_session.query(models.ArticleWithComments).filter(models.ArticleWithComments.id == article_id).all()
    if not article:
        raise exceptions.ArticleDoesNotExists
    comments = list(filter(lambda curr_article: not bool(curr_article.reply_id), article[0].comments))
    return comments
