from pydantic import BaseModel

class WorkflowResponse(BaseModel):
    workflow_id: str
    name: str

    class Config:
        from_attributes = True
