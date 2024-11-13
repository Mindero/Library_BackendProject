from typing import Type

from sqlalchemy import text, insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.project.core.config import settings
from src.project.models.publisher import Publishers
from src.project.schemas.publisherSchema import PublisherSchema, PublisherCreateUpdateSchema
from src.project.core.exceptions.PublisherException import PublisherAlreadyExists, PublisherNotFound

class PublishersRepository:
    _collection: Type[Publishers] = Publishers

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_publishers(
            self,
            session: AsyncSession,
    ) -> list[PublisherSchema]:
        query = select(self._collection)

        publishers = await session.scalars(query)

        return [PublisherSchema.model_validate(obj=publisher) for publisher in publishers.all()]

    async def create_publisher(
            self,
            session: AsyncSession,
            publisher: PublisherCreateUpdateSchema,
    ) -> PublisherSchema:
        query = (
            insert(self._collection)
            .values(publisher.model_dump())
            .returning(self._collection)
        )

        try:
            created_publisher = await session.scalar(query)
            await session.commit()
        except IntegrityError:
            raise PublisherAlreadyExists(inn=publisher.inn)

        return PublisherSchema.model_validate(obj=created_publisher)

    async def update_publisher(
            self,
            session: AsyncSession,
            publisher_id: int,
            publisher: PublisherCreateUpdateSchema,
    ) -> PublisherSchema:
        query = (
            update(self._collection)
            .where(self._collection.id_publisher == publisher_id)
            .values(publisher.model_dump())
            .returning(self._collection)
        )

        try:
            updated_publisher = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise PublisherAlreadyExists(inn=publisher.inn)

        return PublisherSchema.model_validate(obj=updated_publisher)

    async def delete_publisher(
            self,
            session: AsyncSession,
            publisher_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id_publisher == publisher_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise PublisherNotFound(_id=publisher_id)