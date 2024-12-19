from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from project.core.enums.Role import Role
from src.project.api.depends import database, author_repo, RoleChecker
from src.project.core.exceptions.AuthorExceptions import AuthorNotFound
from src.project.schemas.authorSchema import AuthorSchema, AuthorCreateUpdateSchema

router = APIRouter()


@router.get("/all_authors", response_model=list[AuthorSchema])
async def get_all_authors() -> list[AuthorSchema]:
    async with database.session() as session:
        all_author = await author_repo.get_all_authors(session=session)

    return all_author


@router.get("/{author_id}", response_model=AuthorSchema)
async def get_author_by_id(author_id: int) -> AuthorSchema:
    try:
        async with database.session() as session:
            author = await author_repo.get_by_id(session=session, author_id=author_id)
    except AuthorNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return author


@router.post("/add_author", response_model=AuthorSchema, status_code=status.HTTP_201_CREATED)
async def add_author(
        author_dto: AuthorCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> AuthorSchema:
    try:
        async with database.session() as session:
            new_author = await author_repo.create_author(session=session, author=author_dto)
    except AuthorNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_author


@router.put(
    "/update_author/{author_id}",
    response_model=AuthorSchema,
    status_code=status.HTTP_200_OK,
)
async def update_author(
        author_id: int,
        author_dto: AuthorCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> AuthorSchema:
    try:
        async with database.session() as session:
            updated_author = await author_repo.update_author(
                session=session,
                author_id=author_id,
                author=author_dto,
            )
    except AuthorNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_author


@router.delete("/delete_author/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
        author_id: int,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> None:
    try:
        async with database.session() as session:
            author = await author_repo.delete_author(session=session, author_id=author_id)
    except AuthorNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    await session.commit()
    return author
