from typing import Any

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDBase[
    ModelType: SQLModel,
    CreateSchemaType: SQLModel,
    UpdateSchemaType: SQLModel,
]:
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> ModelType | None:
        """根据 id 获取单个对象"""
        return await db.get(self.model, id)

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        """获取列表(分页)"""
        statement = select(self.model).offset(skip).limit(limit)
        result = await db.exec(statement)
        return result.all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """创建对象"""
        db_obj = self.model.model_validate(obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict | str,
    ) -> ModelType:
        """更新对象"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        db_obj.sqlmodel_update(update_data)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
