from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class TariffConfig(BaseModel):
    plan_1: str = "plan_1 месяц"
    plan_3: str = "plan_3 месяца"
    plan_6: str  = "plan_6 месяцев"

class ChannelConfig(BaseModel):
    chan_id: int

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
    channel: ChannelConfig

settings = Settings()
tariff = TariffConfig()