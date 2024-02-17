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