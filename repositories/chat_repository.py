from database import db
from typing import List

class ChatRepository:
    async def get_chats_by_user(self, user_id: str) -> List[dict]:
        query = """
            SELECT id, title, last_used_at, workflow_id 
            FROM chats 
            WHERE user_id = $1 AND is_active = true
            ORDER BY last_used_at DESC
        """
        # We need to cast the user_id to UUID in Postgres, or pass it directly if asyncpg handles it
        # Assuming asyncpg handles string to uuid automatically if type is UUID, 
        # but safely we can do: WHERE user_id = $1::uuid
        query = """
            SELECT id, title, last_used_at, workflow_id 
            FROM chats 
            WHERE user_id = $1::uuid AND is_active = true
            ORDER BY last_used_at DESC
        """
        records = await db.query(query, user_id)
        return [dict(record) for record in records] if records else []

chat_repository = ChatRepository()
