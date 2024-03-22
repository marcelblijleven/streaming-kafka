from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bootstrap_servers: str
    group_id: str

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
    )
