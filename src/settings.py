from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BD_NAME: str
    BD_HOST: str
    BD_PORT: str
    BD_USERNAME: str
    BD_PASSWORD: str
    ROOT_PATH: str
    SECRET_KEY: str
    HASH_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    RESET_TOKEN_EXPIRE_MINUTES: int
    MAIL_HOST: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str

    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env")


settings: Settings = Settings()  # type: ignore
