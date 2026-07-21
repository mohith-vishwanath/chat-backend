from fastapi import APIRouter, Depends
from typing import List
from schemas.workflow_schemas import WorkflowResponse
from schemas.auth_schemas import TokenPayload
from services.workflow_service import workflow_service
from dependencies.auth_deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[WorkflowResponse])
async def get_workflows(current_user: TokenPayload = Depends(get_current_user)):
    """
    Fetch all active workflows.
    """
    workflows = await workflow_service.get_active_workflows()
    return workflows
