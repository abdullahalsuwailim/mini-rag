from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


def get_settings():
    return Settings()