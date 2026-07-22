from fastapi import HTTPException, status
from schemas.auth_schemas import UserLogin, Token
from repositories.auth_repository import AuthRepository
from core.security import verify_password, create_access_token

class AuthService:
    def __init__(self):
        self.repository = AuthRepository()

    async def authenticate_user(self, login_data: UserLogin) -> Token:
        user_record = await self.repository.get_user_by_email(login_data.email)
        
        if not user_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not verify_password(login_data.password, user_record["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        if not user_record["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user",
            )

        # Generate JWT with user_id and email
        token_data = {
            "user_id": str(user_record["id"]),
            "email": user_record["email"]
        }
        access_token = create_access_token(data=token_data)
        
        return Token(access_token=access_token)
