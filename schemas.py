from pydantic import BaseModel, Field, validator
from typing import Optional
import re

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
