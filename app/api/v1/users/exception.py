from fastapi import HTTPException


class AuthException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=403, detail=detail)
