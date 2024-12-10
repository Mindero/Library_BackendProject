from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.project.api.authorization.hash import oauth2_scheme_login
from src.project.api.authorization.token_service import create_access_token
from src.project.core.config import settings
from src.project.core.enums.Role import Role
from src.project.core.exceptions.AuthorizationException import AuthorizationException
from src.project.schemas.tokenSchema import Token
from src.project.api.depends import database, reader_repo, get_current_reader, RoleChecker
from src.project.core.exceptions.ReaderExceptions import ReaderNotFound
from src.project.schemas.readerInDB import ReaderInDB, ReaderCreateUpdateSchema, ReaderLoginSchema, \
    ReaderRegisterSchema

router = APIRouter()


@router.get("/all_readers", response_model=list[ReaderInDB])
async def get_all_readers(_: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN]))]) -> list[ReaderInDB]:
    async with database.session() as session:
        await reader_repo.check_connection(session=session)
        all_readers = await reader_repo.get_all_readers(session=session)

    return all_readers


@router.get("/{reader_id}",
            response_model=ReaderInDB,
            status_code=status.HTTP_200_OK)
async def get_reader_by_id(reader: ReaderInDB = Depends(get_current_reader)) -> ReaderInDB:
    return reader


@router.post("/add_reader", response_model=ReaderInDB, status_code=status.HTTP_201_CREATED)
async def add_reader(
        reader_dto: ReaderCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN]))]
) -> ReaderInDB:
    try:
        async with database.session() as session:
            new_reader = await reader_repo.create_reader(session=session, reader=reader_dto)
    except ReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_reader


@router.put(
    "/update_reader/{reader_id}",
    response_model=ReaderInDB,
    status_code=status.HTTP_200_OK,
)
async def update_reader(
        reader_id: int,
        reader_dto: ReaderCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN]))]
) -> ReaderInDB:
    try:
        async with database.session() as session:
            updated_reader = await reader_repo.update_reader(
                session=session,
                reader_id=reader_id,
                reader=reader_dto,
            )
    except ReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_reader


@router.delete("/delete_reader/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reader(
        reader_id: int,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN]))]
) -> None:
    try:
        async with database.session() as session:
            reader = await reader_repo.delete_reader(session=session, reader_id=reader_id)
    except ReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return reader


@router.post("/auth/login", status_code=status.HTTP_200_OK)
async def login_reader(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    async with database.session() as session:
        reader = await reader_repo.authenticate_reader(
            session=session,
            loginDto=ReaderLoginSchema(email=form_data.username, password=form_data.password))
    token = create_access_token(reader.reader_ticket,
                                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=token, token_type="bearer")


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register_reader(registerDto: ReaderRegisterSchema) -> None:
    try:
        async with database.session() as session:
            await reader_repo.create_reader(session=session, readerRegister=registerDto)
    except BaseException as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.args)

