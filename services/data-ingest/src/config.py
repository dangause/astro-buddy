import os
from pydantic_settings import BaseSettings

API_CHAT_STR = "/chat"
API_DATA_STR = "/data"

class Settings(BaseSettings):
    OPENAI_API_KEY: str

    AWS_ACCOUNT_ID: str
    AWS_REGION: str

    POSTGRES_DB_PASSWORD: str
    POSTGRES_DB_HOST: str
    POSTGRES_DB_PORT: str
    POSTGRES_DB_USER: str
    POSTGRES_DB_DBNAME: str

    PGVECTOR_COLLECTION_NAME: str

    COSINE_THRESHOLD: float = 0

    CORS_ORIGINS: list[str]
    CORS_HEADERS: list[str]

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}" + "/../../.env"
        env_file_encoding = "utf-8"


settings = Settings()