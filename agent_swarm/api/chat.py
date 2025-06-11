from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from agent_swarm.manager.manager import Manager

router = APIRouter()
manager = Manager()

class ChatRequest(BaseModel):
    message: str    
    user_id: str

class ChatResponse(BaseModel):
    response: str
    source_agent_response: str
    agent_workflow: list

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    message = request.message
    try:
        ChatResponse = await manager.chat(message)
        return ChatResponse
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))