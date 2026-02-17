from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class AdminConfig(BaseModel):
    support: str
    super_user: str

class PaymentConfig(BaseModel):
    token: str

class ChannelConfig(BaseModel):
    chan_id: int

class RunConfig(BaseModel):
    token: str

class DatabaseConfig(BaseModel):
    url: PostgresDsn

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="SUBSCRIBE__",
        env_file="../.env",
    )

    run: RunConfig
    db: DatabaseConfig
    channel: ChannelConfig
    payment: PaymentConfig
    admin: AdminConfig

settings: Settings = Settings()