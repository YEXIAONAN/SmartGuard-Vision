from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "智感护航后端平台中枢"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    database_url: str | None = None
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "123456"
    mysql_database: str = "smartguard_vision"

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    auth_secret_key: str = "smartguard-vision-change-me"
    auth_algorithm: str = "HS256"
    auth_access_token_expire_minutes: int = 120
    auth_refresh_token_expire_days: int = 14
    auth_login_rate_limit: int = 5
    auth_login_rate_window_minutes: int = 10
    auth_lock_minutes: int = 5

    default_alert_sla_minutes: int = 30
    default_sensor_temp_threshold: float = 50.0
    default_sensor_smoke_threshold: float = 10.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.database_url:
            return self.database_url
        return "sqlite:///./smartguard_vision.db"

    @property
    def mysql_sqlalchemy_uri(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
