from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user_schemas import UserProfileResponse
from schemas.auth_schemas import TokenPayload
from dependencies.auth_deps import get_current_user
from repositories.auth_repository import AuthRepository

router = APIRouter()
repository = AuthRepository()

@router.get("/", response_model=UserProfileResponse)
async def get_user_profile(current_user: TokenPayload = Depends(get_current_user)):
    """
    Get the profile information of the currently authenticated user.
    """
    user_record = await repository.get_user_by_id(current_user.user_id)
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserProfileResponse(**user_record)
