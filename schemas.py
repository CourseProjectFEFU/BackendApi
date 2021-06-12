from pydantic import BaseModel, Field, validator
from typing import Optional
import re
from datetime import datetime
import models

# for validating an Email
regex = "^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$"


class User(BaseModel):
    first_name: str
    last_name: str
    nickname: str
    email: str

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
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$",
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

    class Config:
        orm_mode = True


class UserForSearchRequest(UserForSearchAnswer):
    offset: Optional[int] = 0
    count: Optional[int] = 15


class LoginResult(RequestResult):
    id: Optional[int]
    username: Optional[int]


class ArticleForAdd(BaseModel):
    header: str
    content: str


class SearchArticle(BaseModel):
    id: Optional[int]
    header: Optional[str]
    content: Optional[str]
    author_id: Optional[str]
    status: int = models.ModerationStatus.published.value
    offset: Optional[int] = 0
    count: Optional[int] = 15


class Article(BaseModel):
    id: int
    header: str
    content: str
    creation_date: str
    publication_date: str
    author_id: int
    status: int

    class Config:
        orm_mode = True
