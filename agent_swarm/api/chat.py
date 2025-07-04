from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from agent_swarm.agents.agent_manager import Manager
import os

router = APIRouter()
manager = Manager(os.getenv('GOOGLE_GEN_AI_KEY'))

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
        chat_response = await manager.chat(message)
        return chat_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))