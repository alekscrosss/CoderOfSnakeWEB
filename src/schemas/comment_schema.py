# file comment_schema.py

from pydantic import BaseModel, EmailStr, Field #18/02/2024 Olha try4
from typing import Optional
from datetime import datetime


class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class Comment(CommentBase):
    id: int
    user_id: int
    photo_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    
class User(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True
