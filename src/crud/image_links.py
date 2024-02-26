from sqlalchemy.orm import Session
from src.db.models import ImageLink
from src.schemas.image_links import ImageLinkCreate

def create_image_link(db: Session, image_link: ImageLinkCreate, url: str, qr_code: str) -> ImageLink:
    db_image_link = ImageLink(photo_id=image_link.photo_id, url=url, qr_code=qr_code)
    db.add(db_image_link)
    db.commit()
    db.refresh(db_image_link)
    return db_image_link