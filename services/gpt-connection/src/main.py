from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.routers.chat import router as chat_router

description = """
Service that handles the creation and querying of Langchain QARetrieval chain.
"""

app = FastAPI(
    title="Astro Buddy LLM Query",
    description=description,
    version = "0.1.0",
)

app.include_router(chat_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://astro-buddy.vercel.app"],  # Or your actual deployed Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", include_in_schema=False, summary="Health check for service")
def health() -> dict[str, str]:
    return {"status": "UP-v1.0"}