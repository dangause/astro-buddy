from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.routers.data_ingest import router as data_router

description = """
Service that handles the parsing, encoding, and ingest of 
data into PostgreSQL astro-buddy-db database with PGVector
"""

app = FastAPI(
    title="Astro Buddy Data Ingest",
    description=description,
    version = "0.1.0",
)

app.include_router(data_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.DATA_INGEST_CORS_ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/health", include_in_schema=False, summary="Health check for service")
def health() -> dict[str, str]:
    return {"status": "UP-v1.0"}