import asyncpg
from core.config import settings

import logging

logger = logging.getLogger("uvicorn")

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=settings.DATABASE_URL)
        logger.info("Connected")

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def query(self, query: str, *args, fetch_one=False):
        if not self.pool:
            raise Exception("Database is not connected")
        async with self.pool.acquire() as connection:
            try:
                if fetch_one:
                    result = await connection.fetchrow(query, *args)
                else:
                    result = await connection.fetch(query, *args)
                return result
            except Exception as e:
                # In a real app you might want to log this error
                raise e

db = Database()
