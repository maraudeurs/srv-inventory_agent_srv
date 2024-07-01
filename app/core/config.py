from pydantic_settings import BaseSettings, SettingsConfigDict
import logging
import os

class Settings(BaseSettings):
    database_url: str
    log_level: str
    app_name: str
    discovery_generic_user: str
    discovery_generic_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

class TestSettings(Settings):
    debug: bool = True

    class Config:
        env_file = "test.env"

def get_settings(env: str) -> Settings:
    if env == "test":
        return TestSettings()
    else:
        return Settings()

env = os.getenv("ENVIRONMENT", "test")
settings = get_settings(env)
