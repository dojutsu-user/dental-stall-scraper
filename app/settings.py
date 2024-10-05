from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # app settings
    app_name: str = Field("Dentalstall Scraper Tool", env="APP_NAME")
    environment: str = Field("development", env="ENVIRONMENT")

    # scraping settings
    proxy: Optional[str] = Field(None, env="PROXY")
    static_token: str = Field(..., env="STATIC_TOKEN")
    max_page_limit: int = Field(10, env="MAX_PAGE_LIMIT")
    images_folder: str = Field("images")

    # redis cache settings
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_db: int = Field(0, env="REDIS_DB")

    # logger settings
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("app.log", env="LOG_FILE")

    # Dentalstall settings
    dentalstall_base_url: str = Field("https://dentalstall.com/shop",
                                      env="DENTALSTALL_BASE_URL")
    dentalstall_max_retries: int = Field(3)

    # output settings
    output_json_filename: str = Field("outputs.json")

    class Config:
        env_file = ".env.dev"


class ProdSettings(Settings):
    class Config:
        env_file = ".env.prod"


def get_settings():
    settings = Settings()
    if settings.environment == "production":
        settings = ProdSettings()
    return settings
