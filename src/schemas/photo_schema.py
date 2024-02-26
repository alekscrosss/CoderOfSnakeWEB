from pydantic import BaseModel, Field
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
        orm_mode = True
