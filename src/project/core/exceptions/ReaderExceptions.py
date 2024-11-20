from typing import Final
from src.project.models.reader import Readers


class ReaderNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Reader с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class ReaderAlreadyExists(BaseException):

    def __init__(self) -> None:
        super().__init__(f"Ошибка при вставке в таблицу {Readers.__tablename__} одного из полей уже существует")
