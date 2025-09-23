from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BD_NAME: str
    BD_HOST: str
    BD_PORT: str
    BD_USERNAME: str
    BD_PASSWORD: str
    ROOT_PATH: str
    # BASE_URL: str

    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env")


settings: Settings = Settings()  # type: ignore
