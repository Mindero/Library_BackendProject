from pydantic import SecretStr
from pydantic_settings import BaseSettings


# Вся конфигурация приложения
class Settings(BaseSettings):
    # TODO: убрать значения по умолчанию при переносе приложения в Docker
    ORIGINS: str = "*"
    ROOT_PATH: str = ""
    ENV: str = "DEV"
    LOG_LEVEL: str = "DEBUG"

    POSTGRES_SCHEMA: str = "my_app_schema"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_DB: str = "postgres"
    POSTGRES_PORT: int = 5436
    POSTGRES_USER: SecretStr = "postgres"
    POSTGRES_PASSWORD: SecretStr = "postgres"
    POSTGRES_RECONNECT_INTERVAL_SEC: int = 1

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def postgres_url(self) -> str:
        creds = f"{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}"
        return f"postgresql+asyncpg://{creds}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
