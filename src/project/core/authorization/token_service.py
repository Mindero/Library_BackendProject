from datetime import timedelta, datetime, timezone
from http.client import HTTPException

import jwt
from jwt import InvalidTokenError
from starlette import status

from project.core.exceptions.AuthorizationException import AuthorizationException
from project.schemas.tokenSchema import TokenData
from src.project.core.config import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def fetch_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        reader_id: int = payload.get("sub")
        if reader_id is None:
            raise AuthorizationException()
        token_data = TokenData(reader_id=reader_id)
        return token_data
    except InvalidTokenError:
        raise AuthorizationException()
