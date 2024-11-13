from typing import Type

from sqlalchemy import text, insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.models.bookInstance import BookInstance
from src.project.schemas.bookInstanceSchema import BookInstanceSchema, BookInstanceCreateUpdateSchema
from src.project.core.exceptions.BookInstanceExceptions import BookInstanceNotFound

class BookInstanceRepository:
    _collection: Type[BookInstance] = BookInstance

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_bookInstance(
            self,
            session: AsyncSession,
    ) -> list[BookInstanceSchema]:
        query = select(self._collection)

        bookInstance = await session.scalars(query)

        return [BookInstanceSchema.model_validate(obj=val) for val in bookInstance.all()]

    async def create_bookInstance(
            self,
            session: AsyncSession,
            bookInstance: BookInstanceCreateUpdateSchema,
    ) -> BookInstanceSchema:
        query = (
            insert(self._collection)
            .values(bookInstance.model_dump())
            .returning(self._collection)
        )

        created_bookInstance = await session.scalar(query)
        await session.commit()

        return BookInstanceSchema.model_validate(obj=created_bookInstance)

    async def update_bookInstance(
            self,
            session: AsyncSession,
            bookInstance_id: int,
            bookInstance: BookInstanceCreateUpdateSchema,
    ) -> BookInstanceSchema:
        query = (
            update(self._collection)
            .where(self._collection.id_instance == bookInstance_id)
            .values(bookInstance.model_dump())
            .returning(self._collection)
        )

        updated_bookInstance = await session.scalar(query)

        if not updated_bookInstance:
            raise BookInstanceNotFound(_id=bookInstance_id)

        return BookInstanceSchema.model_validate(obj=updated_bookInstance)

    async def delete_bookInstance(
            self,
            session: AsyncSession,
            bookInstance_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id_instance == bookInstance_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise BookInstanceNotFound(_id=bookInstance_id)