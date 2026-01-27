from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    token: str

class DatabaseConfig(BaseModel):
    db_url: str

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="SUBSCRIBE__",
        env_file="../.env",
    )

    run: RunConfig
    db: DatabaseConfig

settings = Settings()