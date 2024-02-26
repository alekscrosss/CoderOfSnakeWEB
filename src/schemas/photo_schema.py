# file photo_schema.py
from pydantic import BaseModel, EmailStr, Field #18/02/2024 Olha try4
from typing import Optional
from datetime import datetime

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
