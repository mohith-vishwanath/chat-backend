from typing import List
from repositories.workflow_repository import workflow_repository
from schemas.workflow_schemas import WorkflowResponse

class WorkflowService:
    async def get_active_workflows(self) -> List[WorkflowResponse]:
        workflows_data = await workflow_repository.get_active_workflows()
        return [WorkflowResponse(**data) for data in workflows_data]

workflow_service = WorkflowService()
