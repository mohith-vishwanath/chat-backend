from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from database import db
from endpoints.auth_endpoints import router as auth_router
from dependencies.auth_deps import get_current_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database pool
    await db.connect()
    yield
    # Shutdown: Disconnect the pool
    await db.disconnect()

app = FastAPI(title="Chat Backend API", lifespan=lifespan)

# Include the public auth routes
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

# Example protected route showcasing the JWT middleware
@app.get("/api/protected", dependencies=[Depends(get_current_user)])
async def protected_route():
    return {"message": "You are authenticated and have a valid JWT!"}

# Example protected route extracting user data from JWT
@app.get("/api/me")
async def read_users_me(current_user = Depends(get_current_user)):
    return {"user": current_user}
