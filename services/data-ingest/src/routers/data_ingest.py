"""
File to handle the ingest of arxiv data
"""
import json

from fastapi import APIRouter
from src.config import Settings
from src.core.utils import ingest_arxiv, delete_collection

router = APIRouter()

@router.post("/ingest", tags=["DATA"])
def ingest_arxiv_data():
    result = ingest_arxiv()
    return result

@router.post("/reset-db", tags=["DATA"])
def reset_db():
    result = delete_collection()
    return {'status': result}

