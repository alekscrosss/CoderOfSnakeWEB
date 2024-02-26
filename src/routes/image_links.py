from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.models import SessionLocal, Photo, ImageLink as DBImageLink
from src.schemas.image_links import ImageLink as SchemaImageLink, ImageLinkCreate
from src.crud.image_links import create_image_link
from src.db.database import get_db
import qrcode
from io import BytesIO
import base64

router = APIRouter()

@router.post("/create-link/{photo_id}", response_model=SchemaImageLink)
async def create_image_link_endpoint(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Генерация URL
    url = f"http://localhost:8000/photo/{photo_id}"

    # Генерация QR-кода
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    qr_code_data = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    # Создание записи в базе данных
    image_link_data = ImageLinkCreate(photo_id=photo_id)
    new_link = create_image_link(db=db, image_link=image_link_data, url=url, qr_code=qr_code_data)

    return new_link

@router.get("/get-link/{photo_id}", response_model=SchemaImageLink)
async def get_image_link(photo_id: int, db: Session = Depends(get_db)):
    image_link = db.query(DBImageLink).filter(DBImageLink.photo_id == photo_id).first()
    if image_link is None:
        raise HTTPException(status_code=404, detail="Image link not found")
    return image_link
