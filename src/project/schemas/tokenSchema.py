from datetime import date

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, ConfigDict, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    reader_id: int
