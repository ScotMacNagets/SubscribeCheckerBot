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

class RateLimitConfig(BaseModel):
    limit: int = 2
    window: int = 10
    key_prefix: str = "rl"

class RedisDB(BaseModel):
    rate_limiter: int = 0

class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: RedisDB = RedisDB()
    rate_limiter: RateLimitConfig = RateLimitConfig()

class DatabaseConfig(BaseModel):
    url: PostgresDsn

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="SUBSCRIBE__",
        env_file=(".env.template", ".env"),
    )

    run: RunConfig
    db: DatabaseConfig
    channel: ChannelConfig
    payment: PaymentConfig
    admin: AdminConfig
    redis: RedisConfig = RedisConfig()

settings: Settings = Settings()