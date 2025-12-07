from sqlmodel import Field

from app.models.base import BaseModel, SoftDeleteModel


class User(BaseModel, SoftDeleteModel, table=True):
    __tablename__ = "t_user"

    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(max_length=255)
    hashed_password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
