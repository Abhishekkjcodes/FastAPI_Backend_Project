from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_password: str
    database_username: str
    database_hostname: str
    database_port: str
    database_name: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env")

settings=Settings()

class TestSettings(BaseSettings):
    testing_password: str
    testing_username: str
    testing_hostname: str
    testing_port: str
    testing_name: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env")


