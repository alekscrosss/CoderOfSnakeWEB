# file scr\crud\photo.py
from fastapi import HTTPException
from pathlib import Path
import shutil  # Для копіювання файлів
from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette import status


from src.db.models import Photo
from src.schemas.photo_schema import PhotoUpdate

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
UPLOAD_FOLDER = "uploads"  # Папка для збереження завантажених файлів

def create_photo(db: Session, user_id: int, file: UploadFile, description: str):
    # Створюємо папку для збереження файлів, якщо її ще немає
    upload_folder_path = Path(UPLOAD_FOLDER)
    upload_folder_path.mkdir(parents=True, exist_ok=True)

    # Зберігаємо файл на файловій системі
    file_path = upload_folder_path / file.filename
    with open(file_path, "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)  # Копіюємо дані з потоку файлу у файл

    # Створюємо запис про фотографію в базі даних, зберігаючи шлях до файлу
    photo = Photo(filename=file.filename, description=description, user_id=user_id)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


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