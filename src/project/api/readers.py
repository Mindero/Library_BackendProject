from datetime import timedelta

from fastapi import APIRouter, status, HTTPException

from project.core.authorization.token_service import create_access_token
from project.core.config import settings
from project.core.exceptions.AuthorizationException import AuthorizationException
from project.schemas.tokenSchema import Token
from src.project.api.depends import database, reader_repo
from src.project.core.exceptions.ReaderExceptions import ReaderNotFound
from src.project.schemas.readerInDB import ReaderInDB, ReaderCreateUpdateSchema, ReaderLoginSchema, \
    ReaderRegisterSchema

router = APIRouter()


@router.get("/all_readers", response_model=list[ReaderInDB])
async def get_all_readers() -> list[ReaderInDB]:
    async with database.session() as session:
        await reader_repo.check_connection(session=session)
        all_readers = await reader_repo.get_all_readers(session=session)

    return all_readers


@router.get("/{reader_id}", response_model=ReaderInDB)
async def get_reader_by_id(reader_id: int) -> ReaderInDB:
    try:
        async with database.session() as session:
            reader = await reader_repo.get_by_id(session=session, reader_id=reader_id)
    except ReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return reader


@router.post("/add_reader", response_model=ReaderInDB, status_code=status.HTTP_201_CREATED)
async def add_reader(
        reader_dto: ReaderCreateUpdateSchema,
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
) -> None:
    try:
        async with database.session() as session:
            reader = await reader_repo.delete_reader(session=session, reader_id=reader_id)
    except ReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return reader


@router.post("/auth/login", status_code=status.HTTP_200_OK)
async def login_reader(loginDto: ReaderLoginSchema) -> Token:
    try:
        async with database.session() as session:
            reader = await reader_repo.authenticate_reader(session=session, loginDto=loginDto)
    except AuthorizationException as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ex.message)
    except BaseException as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ex.args)
    token = create_access_token({"sub": reader.reader_ticket},
                                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=token, token_type="bearer")


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register_reader(registerDto: ReaderRegisterSchema) -> None:
    try:
        async with database.session() as session:
            await reader_repo.create_reader(session=session, readerRegister=registerDto)
    except ReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)