from typing import Any


class CustomException(Exception):
    def __init__(
        self,
        code: int = 400,
        message: str | None = None,
        data: Any = None,
    ) -> None:
        self.code = code
        self.message = message or "System error"
        self.data = data


class BadRequestException(CustomException):
    def __init__(self, message: str = "Bad Request", data: Any = None):
        super().__init__(code=400, message=message, data=data)


class NotFoundException(CustomException):
    def __init__(self, message: str = "Not Found", data: Any = None):
        super().__init__(code=404, message=message, data=data)


class ForbiddenException(CustomException):
    def __init__(self, message: str = "Forbidden", data: Any = None):
        super().__init__(code=403, message=message, data=data)


class UnauthorizedException(CustomException):
    def __init__(self, message: str = "Unauthorized", data: Any = None):
        super().__init__(code=401, message=message, data=data)


class SystemException(CustomException):
    def __init__(self, message: str = "System Error", data: Any = None):
        super().__init__(code=500, message=message, data=data)
