from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.config import settings
from app.core.exceptions import CustomException
from app.core.response import Response


async def custom_exception_handler(
    request: Request,
    exc: CustomException,
):
    """捕获业务自定义异常, HTTP 状态码始终返回 200"""
    return JSONResponse(
        status_code=200,
        content=Response(
            code=exc.code,
            message=exc.message,
            data=exc.data,
        ).model_dump(),
    )


async def system_exception_handler(
    request: Request,
    exc: Exception,
):
    """捕获未知系统异常"""
    if settings.ENVIRONMENT in ["local", "development"]:
        error_msg = str(exc)
    else:
        error_msg = "Internal Server Error"
    logger.error(exc)
    return JSONResponse(
        status_code=200,
        content=Response(
            code=500,
            message=error_msg,  # 生产环境屏蔽细节
            data=None,
        ).model_dump(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """重写 FastAPI 默认的 422 参数校验错误"""
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"])
        msg = error["msg"]
        errors.append(f"{field}: {msg}")
    return JSONResponse(
        status_code=200,
        content=Response(
            code=422,
            message=" | ".join(errors),
            data=exc.errors(),
        ).model_dump(),
    )
