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
