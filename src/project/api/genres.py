from fastapi import APIRouter, status, HTTPException

from src.project.api.depends import database, genre_repo
from src.project.core.exceptions.GenreExceptions import GenreAlreadyExists, GenreNotFound
from src.project.schemas.genreSchema import GenreSchema, GenreCreateUpdateSchema

router = APIRouter()


@router.get("/all_genres", response_model=list[GenreSchema])
async def get_all_genres() -> list[GenreSchema]:
    async with database.session() as session:
        await genre_repo.check_connection(session=session)
        all_genres = await genre_repo.get_all_genres(session=session)

    return all_genres


@router.post("/add_genre", response_model=GenreSchema, status_code=status.HTTP_201_CREATED)
async def add_genre(
        genre_dto: GenreCreateUpdateSchema,
) -> GenreSchema:
    try:
        async with database.session() as session:
            new_genre = await genre_repo.create_genre(session=session, genre=genre_dto)
    except GenreAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_genre


@router.put(
    "/update_genre/{genre_id}",
    response_model=GenreSchema,
    status_code=status.HTTP_200_OK,
)
async def update_genre(
        genre_id: int,
        genre_dto: GenreCreateUpdateSchema,
) -> GenreSchema:
    try:
        async with database.session() as session:
            updated_genre = await genre_repo.update_genre(
                session=session,
                genre_id=genre_id,
                genre=genre_dto,
            )
    except GenreNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_genre


@router.delete("/delete_genre/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(
        genre_id: int,
) -> None:
    try:
        async with database.session() as session:
            genre = await genre_repo.delete_genre(session=session, genre_id=genre_id)
    except GenreNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return genre
