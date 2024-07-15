from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    database_url: str
    log_level: str = "INFO"
    log_output: str = "stdout"
    log_file: str = "/var/log/srv_inventory_clt.log"
    app_name: str = "inventory_agent_srv"
    discovery_generic_user: str
    discovery_generic_password: str
    admin_username: str
    admin_email: str = ""
    admin_password: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int ="60"
    default_ssh_user: str

    class Config:
        ## don't pass file, will load from os env var
        pass

class TestSettings(Settings):
    debug: bool = True
    log_level: str = "DEBUG"
    log_output: str = "stdout"

    class Config:
        env_file = "test.env"

def get_settings(env: str) -> Settings:
    if env == "test":
        return TestSettings()
    else:
        return Settings()

env = os.getenv("ENVIRONMENT", "test")
settings = get_settings(env)