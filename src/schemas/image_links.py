from pydantic import BaseModel

class ImageLinkBase(BaseModel):
    photo_id: int

class ImageLinkCreate(ImageLinkBase):
    pass

class ImageLink(BaseModel):
    id: int
    photo_id: int
    url: str
    qr_code: str

    class Config:
        from_attributes = True