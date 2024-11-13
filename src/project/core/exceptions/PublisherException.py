from typing import Final


class PublisherNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Publisher с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class PublisherAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Издатель с ИНН '{inn}' уже существует"

    def __init__(self, inn: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(inn=inn)
        super().__init__(self.message)
