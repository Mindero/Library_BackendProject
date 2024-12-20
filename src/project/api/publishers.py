from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from src.project.api.depends import database, publisher_repo, RoleChecker
from src.project.core.exceptions.PublisherException import PublisherAlreadyExists, PublisherNotFound
from src.project.schemas.publisherSchema import PublisherSchema, PublisherCreateUpdateSchema
from src.project.core.enums.Role import Role

router = APIRouter()


@router.get("/all_publishers", response_model=list[PublisherSchema])
async def get_all_publishers() -> list[PublisherSchema]:
    async with database.session() as session:
        await publisher_repo.check_connection(session=session)
        all_publishers = await publisher_repo.get_all_publishers(session=session)

    return all_publishers


@router.get("/{publisher_id}", response_model=PublisherSchema)
async def get_publisher_by_id(publisher_id: int) -> PublisherSchema:
    try:
        async with database.session() as session:
            publisher = await publisher_repo.get_by_id(session=session, bookPublisher_id=publisher_id)
    except PublisherNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return publisher


@router.post("/add_publisher", response_model=PublisherSchema, status_code=status.HTTP_201_CREATED)
async def add_publisher(
        publisher_dto: PublisherCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> PublisherSchema:
    try:
        async with database.session() as session:
            new_publisher = await publisher_repo.create_publisher(session=session, publisher=publisher_dto)
    except PublisherAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_publisher


@router.put(
    "/update_publisher/{publisher_id}",
    response_model=PublisherSchema,
    status_code=status.HTTP_200_OK,
)
async def update_publisher(
        publisher_id: int,
        publisher_dto: PublisherCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> PublisherSchema:
    try:
        async with database.session() as session:
            updated_publisher = await publisher_repo.update_publisher(
                session=session,
                publisher_id=publisher_id,
                publisher=publisher_dto,
            )
    except PublisherNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_publisher


@router.delete("/delete_publisher/{publisher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_publisher(
        publisher_id: int,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> None:
    try:
        async with database.session() as session:
            publisher = await publisher_repo.delete_publisher(session=session, publisher_id=publisher_id)
    except PublisherNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return publisher
