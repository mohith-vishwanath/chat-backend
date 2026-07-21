from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from database import db
from endpoints.auth_endpoints import router as auth_router
from endpoints.workflow_endpoints import router as workflow_router
from endpoints.chat_endpoints import router as chat_router
from dependencies.auth_deps import get_current_user
from services.secrets_service import secrets_service

import logging

logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load secrets first
    secrets_service.load_secrets()
    # Startup: Connect to the database pool
    await db.connect()
    logger.info("Server started, listening on port 8000")
    yield
    # Shutdown: Disconnect the pool
    await db.disconnect()

app = FastAPI(title="Chat Backend API", lifespan=lifespan)

# Include the public auth routes
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(workflow_router, prefix="/api/workflows", tags=["workflows"])
app.include_router(chat_router, prefix="/api/chats", tags=["chats"])

@app.get("/health")
async def health_check():
    return {"message": "Stay Hungry, Stay Foolish"}

# Example protected route showcasing the JWT middleware
@app.get("/api/protected", dependencies=[Depends(get_current_user)])
async def protected_route():
    return {"message": "You are authenticated and have a valid JWT!"}

# Example protected route extracting user data from JWT
@app.get("/api/me")
async def read_users_me(current_user = Depends(get_current_user)):
    return {"user": current_user}
