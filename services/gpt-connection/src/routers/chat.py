# from fastapi import APIRouter
# from fastapi.responses import JSONResponse

# from src.schemas.Inputs import Chat
# from src.core.utils import ask

# router = APIRouter()

# @router.post("/chat-rag", tags=["CHAT"])
# def query_rag(chat: Chat):
#     response = ask(chat.userInput)
#     response_object = {"response":response}
#     return JSONResponse(content = response_object)

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from src.core.utils import ask

router = APIRouter()

class ChatRequest(BaseModel):
    userInput: str

@router.post("/chat-rag")
def query_rag(chat: ChatRequest, request: Request):
    auth_header = request.headers.get("authorization")
    api_key = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None
    deployment = request.headers.get("x-deployment-name")
    api_base = request.headers.get("x-api-base")
    api_version = request.headers.get("x-api-version")

    if not api_key:
        raise HTTPException(status_code=400, detail="Missing OpenAI API key")

    try:
        response = ask(chat.userInput, api_key, deployment, api_base, api_version)
        return {"response": response}  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

