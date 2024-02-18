from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Optional[str] = None


# Iuliia 18.02.24 -  Photo
class PhotoBase(BaseModel):
    description: str


class PhotoCreate(PhotoBase):
    id: int
    filename: str


class PhotoUpdate(PhotoBase):
    id: int
    filename: str


class Photo(PhotoBase):
    id: int
    filename: str

    class Config:
        orm_mode = True
