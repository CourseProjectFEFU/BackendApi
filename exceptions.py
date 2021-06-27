from fastapi import Request
from fastapi.responses import JSONResponse
from main import app


class NicknameAlreadyExists(Exception):
    pass


class EmailAlreadyExists(Exception):
    pass


class UserDoesNotExists(Exception):
    pass


class UserIsBanned(Exception):
    pass


class PermissionDenied(Exception):
    pass


class ArticleDoesNotExists(Exception):
    pass


class CommentDoesNotExists(Exception):
    pass


class UnexpectedError(Exception):
    pass


class UserAccountIsNotVerified(Exception):
    pass


class InvalidCategory(Exception):
    pass


@app.exception_handler(NicknameAlreadyExists)
async def nickname_already_exists_exception_handler(
    request: Request, ex: NicknameAlreadyExists
):
    return JSONResponse(
        status_code=400,
        content={"result": "error", "error_description": "Nickname already exists"},
    )


@app.exception_handler(EmailAlreadyExists)
async def nickname_already_exists_exception_handler(
    request: Request, ex: NicknameAlreadyExists
):
    return JSONResponse(
        status_code=400,
        content={"result": "error", "error_description": "Email already exists"},
    )


@app.exception_handler(UserDoesNotExists)
async def user_does_not_exists_exception_handler(
    request: Request, ex: UserDoesNotExists
):
    return JSONResponse(
        status_code=405,
        content={"result": "error", "error_description": "User does not exist"},
    )


@app.exception_handler(UserIsBanned)
async def user_is_banned_exception_handler(request: Request, ex: UserIsBanned):
    return JSONResponse(
        status_code=405,
        content={"result": "error", "error_description": "User is banned"},
    )


@app.exception_handler(PermissionDenied)
async def user_is_banned_exception_handler(request: Request, ex: PermissionDenied):
    return JSONResponse(
        status_code=405,
        content={"result": "error", "error_description": "Permission denied"},
    )


@app.exception_handler(ArticleDoesNotExists)
async def article_does_nor_exists_exception_handler(
    request: Request, ex: ArticleDoesNotExists
):
    return JSONResponse(
        status_code=405,
        content={"result": "error", "error_description": "Article does not exists"},
    )


@app.exception_handler(CommentDoesNotExists)
async def comment_does_not_exists_exception_handler(
    request: Request, ex: CommentDoesNotExists
):
    return JSONResponse(
        status_code=405,
        content={"result": "error", "error_description": "Comment does not exists"},
    )


@app.exception_handler(UnexpectedError)
async def unexpected_error_exception_handler(request: Request, ex: UnexpectedError):
    return JSONResponse(
        status_code=500,
        content={"result": "error", "error_description": "Unexpected server error"},
    )


@app.exception_handler(UserAccountIsNotVerified)
async def user_account_is_not_verified_exception_handler(
    request: Request, ex: UserAccountIsNotVerified
):
    return JSONResponse(
        status_code=401,
        content={
            "result": "error",
            "error_description": "User account is not verified",
        },
    )


@app.exception_handler(InvalidCategory)
async def invalid_category_exception_handler(request: Request, ex: InvalidCategory):
    return JSONResponse(
        status_code=405,
        content={"result": "error", "error_description": "Category does not exist"},
    )
