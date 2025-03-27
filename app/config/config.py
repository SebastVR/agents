import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

ENVIRONMENTS = {
    "dev": ".env.dev",
    "prod": ".env.prod",
}


def load_provided_env() -> None:
    """Load the env file provided on execution time."""

    for _, env_file in ENVIRONMENTS.items():
        if os.getenv("APP_ENV") is not None:
            return
        load_dotenv(
            dotenv_path=env_file,
            override=True,
        )


class Settings(BaseSettings):
    # App settings that match with the .env.x file
    # openai_api_key: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str
    model_name: str
    lite_api_base: str
    lite_llm_set: str

    def __init__(self, env_file: str) -> None:
        super().__init__()
        self.Config.env_file = env_file

    class Config:
        env_file = None


load_provided_env()
ENV_FILE = (
    ENVIRONMENTS["prod"] if os.getenv("APP_ENV") == "prod" else ENVIRONMENTS["dev"]
)
settings = Settings(env_file=ENV_FILE)
