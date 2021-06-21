from pydantic import BaseModel, Field, validator
from typing import Optional, List
import re
from datetime import datetime
import models

# for validating an Email
regex = "^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,4}$"


class User(BaseModel):
    first_name: str
    last_name: str
    nickname: str
    email: str
    subscribed: Optional[bool]

    @validator("email")
    def validate_email(cls, value):
        re.search(regex, value)
        if re.search(regex, value):
            return value
        raise ValueError("Invalid email")

    class Config:
        orm_mode = True


class CreateUser(User):
    password: str

    @validator("password")
    def validate_password(cls, value):
        if re.fullmatch(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&.,])[A-Za-z\d@.,$!#%*?&]{6,20}$",
            value,
        ):
            return value
        raise ValueError("Password is too easy or contains inappropriate symbols")


class RequestResult(BaseModel):
    result: str = Field(description='"success" or "error"')
    error_description: Optional[str] = Field(description="In case of error")
    success_description: Optional[str] = Field(
        description="Sometimes in case of success"
    )


class ChangingTypeUser(BaseModel):
    identifier: str = Field(description="email or nickname")


class UserForSearchAnswer(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    nickname: Optional[str]
    email: Optional[str]
    account_image: Optional[str]
    subscribed: Optional[bool]

    class Config:
        orm_mode = True


class UserForSearchRequest(UserForSearchAnswer):
    offset: Optional[int] = 0
    count: Optional[int] = 15


class SelfInfoAnswer(UserForSearchAnswer):
    type: Optional[models.UserType]


class LoginResult(RequestResult):
    id: Optional[int]
    username: Optional[int]


class ArticleForAdd(BaseModel):
    image: str
    header: str
    content: str


class SearchArticle(BaseModel):
    id: Optional[int]
    header: Optional[str] = ""
    content: Optional[str] = ""
    author_id: Optional[int]
    status: int = models.ModerationStatus.published.value
    offset: Optional[int] = 0
    count: Optional[int] = 15


class Article(BaseModel):
    id: int
    image: str
    header: str
    content: str
    creation_date: datetime
    publication_date: Optional[datetime]
    author_id: int
    status: models.ModerationStatus

    class Config:
        orm_mode = True


class AddComment(BaseModel):
    reply_id: Optional[int]
    content: str
    article_id: int


class Comment(BaseModel):
    id: int
    reply_id: Optional[int]
    content: str
    creation_date: datetime
    status: models.ModerationStatus
    author_id: int
    article_id: int
    replies: List["Comment"]

    class Config:
        orm_mode = True


Comment.update_forward_refs()
