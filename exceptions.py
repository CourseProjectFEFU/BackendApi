from fastapi import Request
from fastapi.responses import JSONResponse
from main import app


class NicknameAlreadyExists(Exception):
    pass


class EmailAlreadyExists(Exception):
    pass


@app.exception_handler(NicknameAlreadyExists)
async def nickname_already_exists_exception_handler(request: Request, ex:NicknameAlreadyExists):
    return JSONResponse(
        status_code=400,
        content={"result":"error", "error_type":"Nickname already exists"}
    )


@app.exception_handler(EmailAlreadyExists)
async def nickname_already_exists_exception_handler(request: Request, ex:NicknameAlreadyExists):
    return JSONResponse(
        status_code=400,
        content={"result":"error", "error_type":"Email already exists"}
    )