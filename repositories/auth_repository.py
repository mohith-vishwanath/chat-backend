from database import db
from typing import Optional

class AuthRepository:
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        query = """
            SELECT id, first_name, last_name, email, is_active, password_hash, auth_source, created_at
            FROM users
            WHERE email = $1;
        """
        record = await db.query(query, email, fetch_one=True)
        return dict(record) if record else None
