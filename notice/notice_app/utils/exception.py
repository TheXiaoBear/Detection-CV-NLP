from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import Response


async def http_exception_handler(
    request: Request,
    exc: Exception
) -> Response:

    if isinstance(exc, HTTPException):

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail,
                "data": None
            }
        )

    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "Internal Server Error",
            "data": None
        }
    )


async def global_exception_handler(
    request: Request,
    exc: Exception
) -> Response:

    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "Internal Server Error",
            "data": None
        }
    )