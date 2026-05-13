from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    postgres_user: str | None = Field(default=None, alias="POSTGRES_USER")
    postgres_password: str | None = Field(default=None, alias="POSTGRES_PASSWORD")
    postgres_host: str | None = Field(default=None, alias="POSTGRES_HOST")
    postgres_port: str | None = Field(default=None, alias="POSTGRES_PORT")
    postgres_db: str | None = Field(default=None, alias="POSTGRES_DB")
    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    users_service_url: str | None = Field(default=None, alias="USERS_SERVICE_URL")

    jwt_secret: str = Field(default="change-me-in-production", alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60 * 24,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    @computed_field
    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.database_url:
            return self.database_url
        if not all(
            [
                self.postgres_user,
                self.postgres_password is not None,
                self.postgres_host,
                self.postgres_port,
                self.postgres_db,
            ]
        ):
            raise ValueError(
                "Set DATABASE_URL or all of POSTGRES_USER, POSTGRES_PASSWORD, "
                "POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB"
            )
        user = quote_plus(self.postgres_user)
        password = quote_plus(self.postgres_password or "")
        return (
            f"postgresql+psycopg://{user}:{password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
