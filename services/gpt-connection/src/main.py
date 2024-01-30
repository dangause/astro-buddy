from fastapi import FastAPI
from fastapi.middleware.cors import CorsMiddleware
from src.config import API_DATA_STR

description = """
Service that handles the parsing, encoding, and ingest of 
data into PostgreSQL astro-buddy-db database with PGVector"""

app = FastAPI(
    title="GENAI_Azure_DataIngest",
    description=description,
    version = "0.1.0",
)

app.include_router()