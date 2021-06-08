from sqlalchemy.orm.session import Session
from sqlalchemy import or_
from fastapi import Depends
from fastapi.responses import JSONResponse

from typing import List

from main import app, get_db, manager
import schemas
import exceptions
import models

@app.post("/api/v1/add_article", response_model=schemas.RequestResult)
def add_article(article_model: models.Article, caegories_list: List[int]):
    for
