import os
from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV_FILENAME = os.path.join(".env")


def _get_dotenv_filepath() -> str:
    current_dir = os.path.abspath(__file__)
    app_dir = os.path.dirname(current_dir)
    project_dir = os.path.dirname(app_dir)

    return os.path.join(project_dir, DOTENV_FILENAME)


class Settings(BaseSettings):
    db_url: str
    jwt_secret_key: str
    jwt_refresh_secret_key: str

    model_config = SettingsConfigDict(env_file=_get_dotenv_filepath())


settings = Settings()
