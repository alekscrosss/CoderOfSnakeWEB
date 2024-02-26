# schemas/photo_cloud.py
from pydantic import BaseModel

class Photo(BaseModel):
    url: str
