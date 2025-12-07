from collections.abc import AsyncGenerator

import jwt
import redis.asyncio as redis
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import security
from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.db.session import async_session_factory, redis_pool
from app.models.user import User
from app.services.user_service import UserService

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to yield a session."""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """Dependency to yield a redis connection."""
    client = redis.Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        await (
            client.close()
        )  # 在 redis-py 中，close() 只是释放连接回池子，并不是断开 TCP


async def get_current_user(
    token: str = Depends(reusable_oauth2),  # noqa: B008
    session: AsyncSession = Depends(get_db),  # noqa: B008
) -> User:
    """Dependency to yield the current user.

    Args:
        token (str): The access token.
        session (AsyncSession): The database session.

    Returns:
        User: The current user.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = payload.get("sub")
    except (jwt.InvalidTokenError, ValidationError) as e:
        raise UnauthorizedException(message="Could not validate credentials") from e

    if not token_data:
        raise UnauthorizedException(message="Could not validate credentials")

    user = await UserService.get_by_id(session, user_id=token_data)
    if not user:
        raise UnauthorizedException(message="User not found")

    if not user.is_active:
        raise UnauthorizedException(message="Inactive user")

    return user
