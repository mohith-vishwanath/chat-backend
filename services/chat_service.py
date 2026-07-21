from typing import List
from repositories.chat_repository import chat_repository
from schemas.chat_schemas import ChatResponse
from datetime import datetime

class ChatService:
    async def get_chats(self, user_id: str) -> List[ChatResponse]:
        chats_data = await chat_repository.get_chats_by_user(user_id)
        
        response_list = []
        for data in chats_data:
            # Format the date to 12-Nov-2025
            last_used_at = data.get("last_used_at")
            formatted_date = ""
            if last_used_at:
                if isinstance(last_used_at, str):
                    try:
                        last_used_at = datetime.fromisoformat(last_used_at)
                    except ValueError:
                        pass
                if isinstance(last_used_at, datetime):
                    formatted_date = last_used_at.strftime("%d-%b-%Y")
            
            response_list.append(ChatResponse(
                id=data["id"],
                title=data["title"],
                last_updated_at=formatted_date,
                workflow_id=data["workflow_id"]
            ))
            
        return response_list

chat_service = ChatService()
