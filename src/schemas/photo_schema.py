from pydantic import BaseModel, Field
# file photo_schema.py
from pydantic import BaseModel, EmailStr, Field #18/02/2024 Olha try4
from typing import Optional

class PhotoBase(BaseModel):
    filename: str

class PhotoCreate(PhotoBase):
    description: str
    size_id: int
    size: str = Field(None, alias="size_name")  # Поле для розміру
    effect: str = Field(None, alias="effect_name")  # Поле для ефекту

class PhotoUpdate(BaseModel):
    description: Optional[str] = None


class Photo(PhotoBase):
    id: int
    description: str
    user_id: int

    class Config:
        from_attributes = True
