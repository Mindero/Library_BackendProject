class ForeignKeyNotFound(BaseException):
    message: str

    def __init__(self, table_name : str) -> None:
        self.message = f"Ошибка в таблице {table_name} при добавлении записи из-за отсутствия ForeignKey"
        super().__init__(self.message)
