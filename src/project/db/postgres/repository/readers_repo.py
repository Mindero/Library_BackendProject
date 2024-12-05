from typing import Type, Annotated

from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import text, insert, update, delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.exceptions.ReaderExceptions import ReaderAlreadyExists, ReaderNotFound
from src.project.core.exceptions.AuthorizationException import AuthorizationException
from src.project.models.reader import Readers
from src.project.schemas.readerInDB import ReaderInDB, ReaderCreateUpdateSchema, ReaderLoginSchema, \
    ReaderRegisterSchema, ReaderSchema
from src.project.core.authorization.hash import verify_password, get_password_hash, oauth2_scheme_login
from src.project.core.authorization.token_service import fetch_access_token, create_access_token
from datetime import date

class ReadersRepository:
    _collection: Type[Readers] = Readers

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_readers(
            self,
            session: AsyncSession,
    ) -> list[ReaderInDB]:
        query = select(self._collection)

        readers = await session.scalars(query)

        return [ReaderInDB.model_validate(obj=readers) for readers in readers.all()]

    async def get_by_id(
            self,
            session: AsyncSession,
            reader_id: int
    ) -> ReaderInDB:
        query = select(self._collection).where(self._collection.reader_ticket == reader_id)

        result = await session.scalar(query)

        if not result:
            raise ReaderNotFound(_id=reader_id)

        return ReaderInDB.model_validate(obj=result)

    async def create_reader(
            self,
            session: AsyncSession,
            readerRegister: ReaderRegisterSchema,
    ) -> ReaderInDB:

        reader_data = readerRegister.dict()
        reader_data['created_date'] = date.today()  # Добавляем текущую дату

        # Создаем объект ReaderSchema
        reader: ReaderSchema = ReaderSchema(**reader_data)

        reader.password = get_password_hash(reader.password)

        # TODO: добавить created_date
        query = (
            insert(self._collection)
            .values(reader.model_dump())
            .returning(self._collection)
        )

        try:
            created_reader = await session.scalar(query)
            await session.commit()
        except IntegrityError as e:
            raise ReaderAlreadyExists()

        return ReaderInDB.model_validate(obj=created_reader)

    async def update_reader(
            self,
            session: AsyncSession,
            reader_id: int,
            reader: ReaderCreateUpdateSchema,
    ) -> ReaderInDB:
        query = (
            update(self._collection)
            .where(self._collection.reader_ticket == reader_id)
            .values(reader.model_dump())
            .returning(self._collection)
        )

        updated_reader = await session.scalar(query)

        if not updated_reader:
            raise ReaderNotFound(_id=reader_id)

        return ReaderInDB.model_validate(obj=updated_reader)

    async def delete_reader(
            self,
            session: AsyncSession,
            reader_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.reader_ticket == reader_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise ReaderNotFound(_id=reader_id)

    async def authenticate_reader(
            self,
            session: AsyncSession,
            loginDto: ReaderLoginSchema
    ) -> ReaderInDB:
        query = select(self._collection).where(self._collection.email == loginDto.email)

        result = await session.scalar(query)
        if not result:
            print("User not found, raising AuthorizationException")
            raise AuthorizationException()
        if not verify_password(loginDto.password, result.password):
            print("Password mismatch, raising AuthorizationException")
            raise AuthorizationException()
        return ReaderInDB.model_validate(obj=result)

    async def get_current_user(
            self,
            session: AsyncSession,
            token: Annotated[str, Depends(oauth2_scheme_login)]
    ) -> ReaderInDB:
        token_data = fetch_access_token(token)
        return await self.get_by_id(session=session, reader_id=token_data.reader_id)