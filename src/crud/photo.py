# crud/photo.py
from fastapi import HTTPException
from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from pathlib import Path
from src.db import database
import shutil  # Для копіювання файлів
from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette import status


from src.db.models import Photo
from src.schemas.photo_schema import PhotoUpdate

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
UPLOAD_FOLDER = "uploads"  # Папка для збереження завантажених файлів

# crud/photo.py

import cloudinary.uploader
from sqlalchemy.orm import Session
from src.schemas.photo_schema import PhotoCreate
from fastapi import UploadFile

# crud/photo.py
import cloudinary.uploader

# crud/photo.py
import cloudinary.uploader

def create_photo(user_id: int, description: str, size: str, effect: str, file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    try:
        # Завантаження фотографії у Cloudinary
        uploaded_image = cloudinary.uploader.upload(file.file, folder="Webcore")

        # Збереження фотографії у базі даних
        db_photo = Photo(
            filename=uploaded_image["public_id"],
            description=description,
            size=size,
            effect=effect,
            user_id=user_id
        )
        db.add(db_photo)
        db.commit()
        db.refresh(db_photo)
        return db_photo
    except Exception as e:
        return {"error": str(e)}




# Iuliia 18.02.24
def delete_photo(photo_id: int, db: Session):
    # Отримання фотографії з бази даних за її ідентифікатором
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo:
        # Видалення файлу з папки uploads
        file_path = Path("uploads") / photo.filename
        if file_path.exists():
            file_path.unlink()

        # Видалення фотографії з бази даних
        db.delete(photo)
        db.commit()
        return True  # Повертаємо True, якщо фотографія була успішно видалена
    else:
        return False  # Повертаємо False, якщо фотографія не була знайдена


# Iuliia 18.02.24
def update_photo(db: Session, photo_id: int, photo_data: PhotoUpdate):
    # Отримуємо фото з бази даних за його ідентифікатором
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    # Оновлення інформації про фотографію в базі даних
    photo.description = photo_data.description
    db.commit()
    db.refresh(photo)
    return photo



# Iuliia 18.02.24
def get_photo(db: Session, photo_id: int):
    # Отримання фотографії з бази даних за її ідентифікатором
    return db.query(Photo).filter(Photo.id == photo_id).first()
