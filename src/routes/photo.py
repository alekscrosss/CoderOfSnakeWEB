# routes/photo.py
import json
from pathlib import Path
from fastapi import Request, Path
import os
from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from src.crud.photo import get_photo, update_photo
from src.db import models, database
from src.schemas import photo_schema
from src.db.models import Photo, Role, User #23/02/24 Olha
from fastapi import HTTPException
from src.services import roles #23/02/24 Olha
from src.services.auth import auth_service #23/02/24 Olha
from src.services.roles import RoleAccess #24/02/24 Olha

router = APIRouter()

#Згідно ТЗ користувачі і юзери можуть робити все зі світлинами
allowed_operation_get = roles.RoleAccess([Role.admin, Role.moderator, Role.user]) #23/02/24 Olha
allowed_operation_create = roles.RoleAccess([Role.admin, Role.moderator, Role.user]) #23/02/24 Olha
allowed_operation_update = roles.RoleAccess([Role.admin, Role.moderator, Role.user]) #24/02/24 Olha
allowed_operation_remove = roles.RoleAccess([Role.admin, Role.moderator, Role.user]) #24/02/24 Olha

# Iuliia 18.02.24 Завантаження світлини з описом (POST):


@router.post("/photos/", status_code=status.HTTP_201_CREATED, description="Завантаження світлини з описом")
async def create_photo(user_id: int = Depends(auth_service.get_current_user), description: str = Form(...), file: UploadFile = File(...), 
                       db: Session = Depends(database.get_db),
                       _: RoleAccess = Depends(allowed_operation_create)): #24/02/24 Olha
                     
    # Перевіряємо, чи існує фото з такою самою назвою в базі даних

    user_id = user_id.id

    existing_photo = db.query(Photo).filter(Photo.filename == file.filename).first()
    if existing_photo:
        # Якщо фото вже є у базі даних, видаляємо його з файлової системи користувача
        file_path = Path("uploads") / file.filename
        if file_path.exists():
            file_path.unlink()
        return existing_photo  # Повертаємо існуючу фото з бази даних

    # Якщо фото ще не було завантажено, зберігаємо його в базу даних і на файлову систему
    file_data = file.file.read()
    photo = Photo(filename=file.filename, description=description, user_id=user_id)
    db.add(photo)
    db.commit()
    db.refresh(photo)

    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(file_data)

    return photo

# Iuliia 18.02.24 Видалення світлини (DELETE):
@router.delete("/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT, description="Видалення світлини")
async def delete_photo(photo_id: int, db: Session = Depends(database.get_db),
                       user: User = Depends(auth_service.get_current_user),
                       _: RoleAccess = Depends(allowed_operation_remove)): #24/02/24 Olha

    # Отримання фотографії з бази даних
    photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

     # Видалення файлу з файлової системи
    file_path = os.path.join("uploads", photo.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Видалення фотографії з бази даних
    db.delete(photo)
    db.commit()

    return status.HTTP_204_NO_CONTENT



# Iuliia 18.02.24 Редагування опису світлини (PUT):
@router.put("/photos/{photo_id}", response_model=photo_schema.Photo, 
            status_code=status.HTTP_200_OK, description="Редагування опису світлини")
def update_photo_handler(photo_id: int, photo_data: photo_schema.PhotoUpdate, db: Session = Depends(database.get_db),
                 user: User = Depends(auth_service.get_current_user),
                 _: RoleAccess = Depends(allowed_operation_update)): #24/02/24 Olha
    new_updated_photo = update_photo(db, photo_id, photo_data)     
    return new_updated_photo


# Iuliia 18.02.24 Отримання світлини за унікальним посиланням (GET):
@router.get("/photos/{photo_id}", status_code=status.HTTP_200_OK, description="Отримання світлини за унікальним посиланням")
def get_photo(photo_id: int, db: Session = Depends(database.get_db),
              user: User = Depends(auth_service.get_current_user),
              _: RoleAccess = Depends(allowed_operation_get)): #24/02/24 Olha
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo

#
# @app.post("/upload_image/")
# def upload_image(image_data: dict, db: Session = Depends(get_db)):
#     crud.upload_image(db, image_data)
#     return {"message": "Image uploaded successfully"}
#
# @app.get("/get_image/{image_id}")
# def get_image(image_id: int, db: Session = Depends(get_db)):
#     image = crud.get_image(db, image_id)
#     if image:
#         return image
#     raise HTTPException(status_code=404, detail="Image not found")