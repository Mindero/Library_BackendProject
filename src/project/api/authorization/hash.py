from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme_login = OAuth2PasswordBearer(tokenUrl="api/readers/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as ex:
        print(f"Error verifying password: {ex}")
        return False


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
