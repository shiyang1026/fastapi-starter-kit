from loguru import logger
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import security
from app.core.exceptions import BadRequestException
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: str) -> User | None:
        return await session.get(User, user_id)

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    @staticmethod
    async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
        existing_user = await UserService.get_by_email(session, user_in.email)
        if existing_user:
            raise BadRequestException(message="User with this email already exists")

        db_obj = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=security.get_password_hash(user_in.password),
            is_active=user_in.is_active,
            is_superuser=user_in.is_superuser,
        )

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @staticmethod
    async def authenticate(
        session: AsyncSession, email: str, password: str
    ) -> User | None:
        """验证用户"""
        user = await UserService.get_by_email(session, email)
        if not user:
            logger.warning(f"Login failed: email {email} not found")
            return None

        if not security.verify_password(password, user.hashed_password):
            logger.warning(f"Login failed: incorrect password for email {email}")
            return None

        logger.info(f"User {user.id} logged in successfully")
        return user
