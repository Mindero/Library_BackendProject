from enum import Enum, unique


@unique
class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
