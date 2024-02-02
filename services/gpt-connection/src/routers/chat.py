from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.schemas.Inputs import Chat
from src.core.utils import ask

router = APIRouter()

@router.post("/chat-rag", tags=["CHAT"])
def query_rag(chat: Chat):
    response = ask(chat.userInput)
    response_object = {"response":response}
    return JSONResponse(content = response_object)