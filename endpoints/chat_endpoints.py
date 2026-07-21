from fastapi import APIRouter, Depends
from typing import List
from schemas.chat_schemas import ChatResponse
from schemas.auth_schemas import TokenPayload
from services.chat_service import chat_service
from dependencies.auth_deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ChatResponse])
async def get_chats(current_user: TokenPayload = Depends(get_current_user)):
    """
    Fetch all active chats for the current user.
    """
    chats = await chat_service.get_chats(current_user.user_id)
    return chats
