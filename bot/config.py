from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    bot_token: str
    admin_ids: List[int] = []

    groq_api_key: str
    gemini_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    gemini_model: str = "gemini-1.5-flash"

    database_url: str
    redis_url: str = "redis://redis:6379/0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
