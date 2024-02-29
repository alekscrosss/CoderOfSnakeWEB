# file scr\shemas\tags_shemas.py

from pydantic import BaseModel
from typing import List, Optional


class TagCreate(BaseModel):
    name: str


class Tag(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class PhotoTagsUpdate(BaseModel):
    tags: List[str] = []
