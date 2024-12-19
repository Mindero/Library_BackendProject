from datetime import date

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, ConfigDict, EmailStr

from project.core.enums.Role import Role


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenData(BaseModel):
    reader_id: int
