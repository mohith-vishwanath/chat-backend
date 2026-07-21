from pydantic import BaseModel
from uuid import UUID

class ChatResponse(BaseModel):
    id: UUID
    title: str
    last_updated_at: str
    workflow_id: str

    class Config:
        from_attributes = True
