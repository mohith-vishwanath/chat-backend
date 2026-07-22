from fastapi import APIRouter, Depends
from schemas.auth_schemas import UserLogin, Token
from services.auth_service import AuthService

router = APIRouter()

def get_auth_service():
    return AuthService()

@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, service: AuthService = Depends(get_auth_service)):
    """
    Public route to authenticate a user and return a JWT valid for 7 days.
    """
    return await service.authenticate_user(login_data)
