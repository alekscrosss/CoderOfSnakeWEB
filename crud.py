# crud.py
from fastapi import HTTPException, Depends
import os
from pathlib import Path
import shutil  # Для копіювання файлів
from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette import status

import database
from models import Photo
from schemas import Photo
import models
# from models import Tag
import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
UPLOAD_FOLDER = "uploads"  # Папка для збереження завантажених файлів

def get_user(db: Session, user_id: int):
    # Получаем пользователя по ид
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    # Получаем пользователя по имени
    return db.query(models.User).filter(models.User.username == username).first()


async def create_user(body: schemas.UserModel, db: Session): #19/02/2024
    
    verification_users_count = db.query(models.User).count() #21/02/2024 - Add role

    if verification_users_count == 0:
        new_user = models.User(
            username=body.username,
            password=body.password,
            email=body.email,
            role=models.Role.admin  # Присваиваем роль 'admin'
        )
    else:
        new_user = models.User(
            username=body.username,
            password=body.password,
            email=body.email
        )    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    # Получаем список пользователей
    return db.query(models.User).offset(skip).limit(limit).all()


def verify_password(plain_password, hashed_password):
    # Проверка на правильность пароля
    return pwd_context.verify(plain_password, hashed_password)

#18/02/2024 Olha try 3 
async def get_user_by_email(email: str, db: Session) -> models.User | None: #19/02/2024 fix    
    return db.query(models.User).filter(models.User.email == email).first() #19/02/2024 fix


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
    photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
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
def update_photo(db: Session, photo_id: int, photo_data: schemas.PhotoUpdate):
    # Отримуємо фото з бази даних за його ідентифікатором
    photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    # Оновлення інформації про фотографію в базі даних
    db.query(models.Photo).filter(models.Photo.id == photo_id).update(photo_data.dict())
    db.commit()



# Iuliia 18.02.24
def get_photo(db: Session, photo_id: int):
    # Отримання фотографії з бази даних за її ідентифікатором
    return db.query(models.Photo).filter(models.Photo.id == photo_id).first()


# # 22.02.24 Nazar
# def add_tags(db: Session, tag_names: list):
#     tag_ids = []
#     for tag_name in tag_names:
#         tag = db.query(Tag).filter(Tag.name == tag_name).first()
#         if not tag:
#             tag = Tag(name=tag_name)
#             db.add(tag)
#             db.commit()
#             db.refresh(tag)
#         tag_ids.append(tag.id)
#     return tag_ids
