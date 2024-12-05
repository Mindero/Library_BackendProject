from typing import Final


class AuthorizationException(BaseException):
    TEMPLATE: Final[str] = "Логин или пароль не совпадает"
    message: str

    def __init__(self) -> None:
        self.message = self.TEMPLATE
        super().__init__(self.message)
