from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class ResponseUtil:

    @staticmethod
    def success(
        data=None,
        message="success",
        code=200
    ):

        return JSONResponse(
            status_code=code,
            content={
                "code": code,
                "message": message,
                "content": jsonable_encoder(data)
            }
        )

    @staticmethod
    def error(
        message="error",
        code=400,
        data=None
    ):

        return JSONResponse(
            status_code=code,
            content={
                "code": code,
                "message": message,
                "data": jsonable_encoder(data)
            }
        )