from sqlalchemy.orm import Session
from src.db.models import ImageLink
from src.schemas.image_links import ImageLinkCreate

def create_image_link(db: Session, image_link: ImageLinkCreate, url: str, qr_code: str) -> ImageLink:
    
    """
    The create_image_link function creates a new image link in the database.
        
    
    :param db: Session: Create a database session
    :param image_link: ImageLinkCreate: Create a new image_link object
    :param url: str: Store the url of the image in the database
    :param qr_code: str: Create the qr_code for the image link
    :return: An imagelink object
    :doc-author: Trelent
    """
    db_image_link = ImageLink(photo_id=image_link.photo_id, url=url, qr_code=qr_code)
    db.add(db_image_link)
    db.commit()
    db.refresh(db_image_link)
    return db_image_link