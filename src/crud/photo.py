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
    
    """
    The create_photo function creates a new photo in the database.
    
    :param user_id: int: Specify the user who uploaded the photo
    :param description: str: Set the description of the photo
    :param size: str: Specify the size of the photo
    :param effect: str: Determine the effect that will be applied to the photo
    :param file: UploadFile: Upload the photo file to cloudinary
    :param db: Session: Pass in the database session
    :return: A dict with an error key
    :doc-author: Trelent
    """
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
    """
    The delete_photo function deletes a photo from the database and removes it from the uploads folder.
        Args:
            photo_id (int): The id of the photo to delete.
            db (Session): A database session object.
    
    :param photo_id: int: Specify the photo to be deleted
    :param db: Session: Pass the database session to the function
    :return: True if the photo is deleted and false otherwise
    :doc-author: Trelent
    """
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
    """
    The update_photo function updates the description of a photo in the database.
        Args:
            db (Session): The database session to use for updating the photo.
            photo_id (int): The id of the photo to update.
            photo_data (PhotoUpdate): An object containing information about what should be updated in this particular record.
    
    :param db: Session: Access the database
    :param photo_id: int: Identify the photo that is being updated
    :param photo_data: PhotoUpdate: Pass the data that will be used to update the photo
    :return: A photo model
    :doc-author: Trelent
    """
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
    """
    The get_photo function returns a photo from the database by its id.
    
    :param db: Session: Pass the database session to the function
    :param photo_id: int: Specify the photo id
    :return: A photo object
    :doc-author: Trelent
    """
    return db.query(Photo).filter(Photo.id == photo_id).first()
