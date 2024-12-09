from datetime import timedelta, datetime, timezone
from http.client import HTTPException
from typing import Annotated

import jwt
from fastapi import Depends
from jwt import InvalidTokenError
from starlette import status

from project.api.authorization.hash import oauth2_scheme_login
from project.core.exceptions.AuthorizationException import AuthorizationException
from project.schemas.tokenSchema import TokenData
from src.project.core.config import settings

AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные для авторизации"


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    to_encode = {"sub": str(user_id)}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def fetch_access_token(token: Annotated[str, Depends(oauth2_scheme_login)]) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM])
        print(payload)
        reader_id: int = payload.get("sub")
        if reader_id is None:
            raise AuthorizationException(detail=AUTH_EXCEPTION_MESSAGE)
        token_data = TokenData(reader_id=reader_id)
        return token_data
    except InvalidTokenError as e:
        print("can't parse jwt ", e)
        raise AuthorizationException(detail=AUTH_EXCEPTION_MESSAGE)
