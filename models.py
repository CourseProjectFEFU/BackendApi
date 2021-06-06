from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Binary,
    Float,
    Table,
    Text,
    Enum
)

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.types import UserDefinedType
from sqlalchemy import func
import enum

from db import Base


class UserType(enum.Enum):
    banned = 0
    user = 1
    moderator = 2
    administrator = 3


class ModerationStatus(enum.Enum):
    waiting = 0
    published = 1
    rejected = 2


article_category_association_table = Table('ArticleCategoryAssociations', Base.metadata,
                                           Column('article_id', Integer, ForeignKey('articles.id')),
                                           Column('category_id', Integer, ForeignKey('categories.id'))
                                           )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    type = Column(Enum(UserType), default=UserType.user, nullable=False)
    email = Column(String, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    nickname = Column(String, nullable=False, unique=True)
    account_image = Column(String)
    password = Column(Binary, nullable=False)
    salt = Column(Binary, nullable=False)


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    content = Column(Text, nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    publication_date = Column(DateTime, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ModerationStatus), nullable=False, default=ModerationStatus.waiting)


class ArticleWithCategories(Article):
    CategoryWithArticles = relationship("CategoryWithArticles", secondary=article_category_association_table)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    reply_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    content = Column(Text, nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    status = Column(Enum(ModerationStatus), default=ModerationStatus.waiting, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class CategoryWithArticles(Category):
    articles = relationship("ArticleWithCategories", secondary=article_category_association_table)

