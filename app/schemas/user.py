import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    username: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=8, max_length=40)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str | None = Field(default=None, min_length=8, max_length=40)
    email: EmailStr | None = None


class UserOut(UserBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
