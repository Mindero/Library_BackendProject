from typing import Final


class GenreNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Genre с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class GenreAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Жанр с именем '{inn}' уже существует"

    def __init__(self, inn: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(inn=inn)
        super().__init__(self.message)
