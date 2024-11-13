from typing import Final


class ReaderNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Reader с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class ReaderAlreadyExists(BaseException):

    def __init__(self, msg: str) -> None:
        super().__init__(self.message)

    @staticmethod
    def emailExists(email: str) -> "ReaderAlreadyExists":
        message = f"Читатель с почтой '{email}' уже существует"
        return ReaderAlreadyExists(msg=message)

    @staticmethod
    def phoneNumberExists(phone_number: str) -> "ReaderAlreadyExists":
        message = f"Читатель с телефоном '{phone_number}' уже существует"
        return ReaderAlreadyExists(msg=message)

    @staticmethod
    def passportExists(passport: str) -> "ReaderAlreadyExists":
        message = f"Читатель с паспортом '{passport}' уже существует"
        return ReaderAlreadyExists(msg=message)
