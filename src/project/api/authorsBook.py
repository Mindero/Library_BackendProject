from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from src.project.api.depends import database, authorsBook_repo, RoleChecker
from src.project.core.exceptions.AuthorsBookException import AuthorsBookNotFound
from src.project.schemas.authorsBookSchema import AuthorsBookSchema, AuthorsBookCreateUpdateSchema
from src.project.core.exceptions.ForeignKeyNotFound import ForeignKeyNotFound
from src.project.core.enums.Role import Role

router = APIRouter()


@router.get("/all_authorsBook", response_model=list[AuthorsBookSchema])
async def get_all_authorsBook() -> list[AuthorsBookSchema]:
    async with database.session() as session:
        await authorsBook_repo.check_connection(session=session)
        all_authorsBook = await authorsBook_repo.get_all_authorsBooks(session=session)

    return all_authorsBook


@router.get("/{authors_book_id}", response_model=AuthorsBookSchema)
async def get_authorBook_by_id(authors_book_id: int) -> AuthorsBookSchema:
    try:
        async with database.session() as session:
            authorBook = await authorsBook_repo.get_by_id(session=session, authors_book_id=authors_book_id)
    except AuthorsBookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return authorBook


@router.post("/add_authorBook", response_model=AuthorsBookSchema, status_code=status.HTTP_201_CREATED)
async def add_authorBook(
        author_dto: AuthorsBookCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN]))]
) -> AuthorsBookSchema:
    try:
        async with database.session() as session:
            new_authorBook = await authorsBook_repo.create_authorsBook(session=session, authorsBook=author_dto)
    except AuthorsBookNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except ForeignKeyNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_authorBook


@router.put(
    "/update_authorBook/{authorBook_id}",
    response_model=AuthorsBookSchema,
    status_code=status.HTTP_200_OK,
)
async def update_authorBook(
        authorBook_id: int,
        authorBook_dto: AuthorsBookCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN]))]
) -> AuthorsBookSchema:
    try:
        async with database.session() as session:
            updated_author = await authorsBook_repo.update_author(
                session=session,
                author_id=authorBook_id,
                authorsBook=authorBook_dto,
            )
    except AuthorsBookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    except ForeignKeyNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return updated_author


@router.delete("/delete_authorBook/{authorBook_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_authorBook(
        authorBook_id: int,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN]))]
) -> None:
    try:
        async with database.session() as session:
            authorsBook = await authorsBook_repo.delete_author(session=session, author_id=authorBook_id)
    except AuthorsBookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return authorsBook
