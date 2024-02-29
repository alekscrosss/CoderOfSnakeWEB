# file routers/user.py

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from src.db.models import Role

class UserModel(BaseModel):
    username: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=6, max_length=150)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str    
    role: Role #24/02/20204 Olha
   

    class Config:
        from_attributes = True

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr

