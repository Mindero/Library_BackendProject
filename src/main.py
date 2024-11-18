import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from project.api import authors
from project.api import authorsBook
from project.api import bookGenres
from project.api import bookInstance
from project.api import bookPublisher
from project.api import bookReader
from project.api import books
from project.api import genres
from project.api import penalty
from project.api import publishers
from project.api import readers
from project.core.config import settings

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app_options = {}
    if settings.ENV.lower() == "prod":
        app_options = {
            "docs_url": None,
            "redoc_url": None,
        }
    if settings.LOG_LEVEL in ["DEBUG", "INFO"]:
        app_options["debug"] = True

    app = FastAPI(root_path=settings.ROOT_PATH, **app_options)
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(authors.router, prefix="/api/authors", tags=["Authors APIs"])
    app.include_router(books.router, prefix="/api/books", tags=["Books APIs"])
    app.include_router(readers.router, prefix="/api/readers", tags=["Readers APIs"])
    app.include_router(publishers.router, prefix="/api/publishers", tags=["Publishers APIs"])
    app.include_router(genres.router, prefix="/api/genres", tags=["Genres APIs"])
    app.include_router(authorsBook.router, prefix="/api/authors_book", tags=["Authors_book APIs"])
    app.include_router(bookGenres.router, prefix="/api/book_genres", tags=["Book_genres APIs"])
    app.include_router(bookInstance.router, prefix="/api/book_instance", tags=["Book_instance APIs"])
    app.include_router(bookPublisher.router, prefix="/api/book_publisher", tags=["Book_publisher APIs"])
    app.include_router(bookReader.router, prefix="/api/book_reader", tags=["Book_reader APIs"])
    app.include_router(penalty.router, prefix="/api/penalty", tags=["Penalty APIs"])

    return app


app = create_app()


async def run() -> None:
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    logger.debug(f"{settings.postgres_url}=")
    asyncio.run(run())
