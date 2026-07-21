from pydantic import BaseModel, EmailStr

class UserProfileResponse(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True
