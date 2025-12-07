from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqlalchemy import text

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.exceptions import CustomException
from app.core.handlers import (
    custom_exception_handler,
    system_exception_handler,
    validation_exception_handler,
)
from app.core.response import Response
from app.db.session import async_session_factory, redis_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.ENVIRONMENT in ["local", "development"]:
        logger.info("Swagger UI: http://127.0.0.1:8000/docs")
        logger.info("ReDoc:      http://127.0.0.1:8000/redoc")

    # 检查 PostgreSQL 连接
    try:
        async with async_session_factory() as session:
            await session.exec(text("SELECT 1"))
        logger.info("Database connection established.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")

    # 检查 Redis 连接
    try:
        client = redis.Redis(connection_pool=redis_pool)
        await client.ping()
        logger.info("Redis connection established.")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")

    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # 注册异常处理器
    app.add_exception_handler(CustomException, custom_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, system_exception_handler)

    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/health", response_model=Response)
    async def health_check():
        # data={"status": "ok", "environment": settings.ENVIRONMENT}
        return Response(
            data={
                "status": "ok",
                "environment": settings.ENVIRONMENT,
            }
        )

    return app


app = create_app()
