from database import db
from typing import List

class WorkflowRepository:
    async def get_active_workflows(self) -> List[dict]:
        query = """
            SELECT workflow_id, name 
            FROM workflows 
            WHERE is_active = true
        """
        records = await db.query(query)
        # asyncpg returns Record objects, convert them to dicts
        return [dict(record) for record in records] if records else []

workflow_repository = WorkflowRepository()
