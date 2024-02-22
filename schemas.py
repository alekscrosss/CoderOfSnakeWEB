# schemas.py
from pydantic import BaseModel, EmailStr, Field #18/02/2024 Olha try4
from typing import Optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserModel(BaseModel): #18/02/2024 Olha try4
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6, max_length=50)
    email: EmailStr


# 20.02.24
class UserResponse(BaseModel):
    username: str
    email: str

class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Optional[str] = None

class TokenModel(BaseModel): #18/02/2024 Olha try4
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class RequestEmail(BaseModel): #18/02/2024 Olha try4
    email: EmailStr


# Iuliia 18.02.24 -  Photo
class PhotoBase(BaseModel):
    filename: str
    description: str


class PhotoCreate(PhotoBase):
    pass


class PhotoUpdate(BaseModel):
    description: Optional[str] = None


class Photo(PhotoBase):
    id: int


    class Config:
        orm_mode = True
