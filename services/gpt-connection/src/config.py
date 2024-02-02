import os
from pydantic_settings import BaseSettings, SettingsConfigDict
import dotenv

config_env = dotenv.find_dotenv('.env.config')

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

    DATA_INGEST_CORS_ORIGINS: list[str]
    GPT_CONNECTION_CORS_ORIGINS: list[str]
    CORS_HEADERS: list[str]

    model_config = SettingsConfigDict(env_file=config_env, env_file_encoding='utf-8', extra='allow')


settings = Settings()

