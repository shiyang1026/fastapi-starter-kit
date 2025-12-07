from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import security
from app.core.config import settings
from app.core.deps import get_db
from app.core.exceptions import UnauthorizedException
from app.core.response import Response
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserLogin, UserOut, UserRegister
from app.services.user_service import UserService

router = APIRouter()


@router.post("/login", response_model=Response[Token])
async def login(
    user_in: UserLogin,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    """
    用户登录，获取 Access Token
    """
    user = await UserService.authenticate(
        session=session, email=user_in.email, password=user_in.password
    )
    if not user:
        raise UnauthorizedException("Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    return Response(data=Token(access_token=access_token, token_type="bearer"))


@router.post("/register", response_model=Response[UserOut])
async def register(
    user_in: UserRegister,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    """
    注册新用户
    """
    # 将 UserRegister 转换为 UserCreate，确保 is_superuser 为 False
    user_create = UserCreate(**user_in.model_dump(), is_superuser=False, is_active=True)
    user = await UserService.create_user(session=session, user_in=user_create)
    return Response(data=user)
