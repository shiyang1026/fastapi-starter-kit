import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class UUIDModel(SQLModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )


class TimestampModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow},  # SQLAlchemy 层面自动更新
    )


class SoftDeleteModel(SQLModel):
    """软删除模型 Mixin, 只有需要软删除的业务表才继承它"""

    is_deleted: bool = Field(default=False, index=True)
    deleted_at: datetime | None = Field(default=None, nullable=True)


class BaseModel(UUIDModel, TimestampModel):
    """
    所有业务模型的基类
    """

    pass
