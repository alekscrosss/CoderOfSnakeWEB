# routes/photo.py
import os
import configparser #25.02.24 Iuliia
import cloudinary.uploader #25.02.24 Iuliia
from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from src.crud.photo import get_photo, update_photo, create_photo
from src.db import models, database
from src.db.database import get_db
from src.schemas import photo_schema
from src.db.models import Photo, Role, User, Size, Effect  # 23/02/24 Olha
from fastapi import HTTPException
from src.services import roles #23/02/24 Olha
from src.services.auth import auth_service #23/02/24 Olha
from src.services.roles import RoleAccess #24/02/24 Olha
from src.schemas.photo_schema import PhotoCreate
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
# Вказуємо шлях до файлу конфігурації
config_file_path = 'conf/config.ini'

# Ініціалізуємо об'єкт конфігурації
config = configparser.ConfigParser()
# Зчитуємо дані з файлу конфігурації
config.read(config_file_path)

# Отримуємо значення з конфігурації
CLD_NAME = os.environ.get('CLD_NAME')
CLD_API_KEY = os.environ.get('CLD_API_KEY')
CLD_API_SECRET = os.environ.get('CLD_API_SECRET')

print(CLD_NAME, CLD_API_KEY, CLD_API_SECRET)

# Тепер використовуйте ці значення для налаштування підключення до Cloudinary
cloudinary.config(
    cloud_name=CLD_NAME,
    api_key=CLD_API_KEY,
    api_secret=CLD_API_SECRET
)

#Згідно ТЗ користувачі і юзери можуть робити все зі світлинами
allowed_operation_get = roles.RoleAccess([Role.admin, Role.moderator, Role.user]) #23/02/24 Olha
allowed_operation_create = roles.RoleAccess([Role.admin, Role.moderator, Role.user]) #23/02/24 Olha
allowed_operation_update = roles.RoleAccess([Role.admin, Role.moderator, Role.user]) #24/02/24 Olha
allowed_operation_remove = roles.RoleAccess([Role.admin, Role.moderator, Role.user]) #24/02/24 Olha

# Iuliia 18.02.24 Завантаження світлини з описом (POST):


from fastapi import Query

@router.post("/photos/grayscale/", status_code=status.HTTP_201_CREATED, description="Завантаження світлини з чорно-білим ефектом ")
async def create_photo_grayscale(user_id: int,
                       description: str = Form(...),
                       size_name: str = Form(...),
                       effect_name: str = Form(...),
                       file: UploadFile = File(...),
                       db: Session = Depends(database.get_db)):
    
    # Отримання ID розміру за його назвою
    """
    The create_photo_grayscale function creates a new photo in the database.
    
    :param user_id: int: Identify the user who uploaded the photo
    :param description: str: Get the description of the photo
    :param size_name: str: Get the size id from its name
    :param effect_name: str: Get the id of the effect by its name
    :param file: UploadFile: Receive the file from the client
    :param db: Session: Get the database session
    :return: A photo object
    :doc-author: Trelent
    """
    size = db.query(Size).filter(Size.name == size_name).first()
    if not size:
        raise HTTPException(status_code=404, detail="Size not found")

    # Отримання ID ефекту за його назвою
    effect = db.query(Effect).filter(Effect.name == effect_name).first()
    if not effect:
        raise HTTPException(status_code=404, detail="Effect not found")

    # Формування трансформаційного рядка для Cloudinary
    # Початкові параметри трансформації у вигляді словника
    transformation = [
                    {"width": 500, "height": 500, "crop": "fill"},
                    {"effect": "grayscale"},
                    {"quality": "auto"}
                ]

    # Завантаження фото з необхідними трансформаціями на Cloudinary
    uploaded_image = cloudinary.uploader.upload(
        file.file,
        folder="Webcore",
        transformation=transformation
    )

    # Збереження фото в базі даних з отриманими ID розміру та ефекту
    photo = Photo(
        filename=uploaded_image["public_id"],
        description=description,
        user_id=user_id,
        size_id=size.id,
        effect_id=effect.id,
        url=uploaded_image["url"]
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return photo_schema.Photo(**photo.__dict__)

# Функція для завантаження фото з ефектом старіння
@router.post("/photos/aging/", status_code=status.HTTP_201_CREATED, description="Завантаження світлини з ефектом старіння")
async def upload_photo_with_aging_effect(user_id: int,
                       description: str = Form(...),
                       size_name: str = Form(...),
                       effect_name: str = Form(...),
                       file: UploadFile = File(...),
                       db: Session = Depends(database.get_db)):
    

    # Отримання ID розміру за його назвою
    """
    The upload_photo_with_aging_effect function uploads a photo to the Cloudinary cloud storage service,
        applies an aging effect to it and saves it in the database.
    
    
    :param user_id: int: Identify the user who uploaded the photo
    :param description: str: Set the description of the photo
    :param size_name: str: Get the size id from its name
    :param effect_name: str: Get the id of the effect by its name
    :param file: UploadFile: Upload the file to cloudinary
    :param db: Session: Get access to the database
    :return: A photo_schema
    :doc-author: Trelent
    """
    size = db.query(Size).filter(Size.name == size_name).first()
    if not size:
        raise HTTPException(status_code=404, detail="Size not found")


    # Отримання ID ефекту за його назвою
    effect = db.query(Effect).filter(Effect.name == effect_name).first()
    if not effect:
        raise HTTPException(status_code=404, detail="Effect not found")

    # Формування трансформаційного рядка для Cloudinary
    # Початкові параметри трансформації у вигляді словника
    transformation = [
                    {"width": 500, "height": 500, "crop": "fill"},
                    {"effect": "sepia"},
                    {"quality": "auto"}
                ]

    # Завантаження фото з необхідними трансформаціями на Cloudinary
    uploaded_image = cloudinary.uploader.upload(
        file.file,
        folder="Webcore",
        transformation=transformation
    )

    # Збереження фото в базі даних з отриманими ID розміру та ефекту
    photo = Photo(
        filename=uploaded_image["public_id"],
        description=description,
        user_id=user_id,
        effect_id=effect.id,
        url=uploaded_image["url"]
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return photo_schema.Photo(**photo.__dict__)


# Функція для завантаження фото з розмиттям
@router.post("/photos/blur/", status_code=status.HTTP_201_CREATED, description="Завантаження світлини з розмиттям")
async def upload_photo_with_blur_effect(user_id: int,
                       description: str = Form(...),
                       size_name: str = Form(...),
                       effect_name: str = Form(...),
                       file: UploadFile = File(...),
                       db: Session = Depends(database.get_db)):
    

    # Отримання ID розміру за його назвою
    """
    The upload_photo_with_blur_effect function uploads a photo to Cloudinary,
        applies the blur effect and saves it in the database.
    
    :param user_id: int: Identify the user who uploaded the photo
    :param description: str: Set the description of the photo
    :param size_name: str: Get the size id from the database
    :param effect_name: str: Get the id of the effect from its name
    :param file: UploadFile: Get the file from the request
    :param db: Session: Access the database
    :return: A photo_schema
    :doc-author: Trelent
    """
    size = db.query(Size).filter(Size.name == size_name).first()
    if not size:
        raise HTTPException(status_code=404, detail="Size not found")


    # Отримання ID ефекту за його назвою
    effect = db.query(Effect).filter(Effect.name == effect_name).first()
    if not effect:
        raise HTTPException(status_code=404, detail="Effect not found")

    # Формування трансформаційного рядка для Cloudinary
    # Початкові параметри трансформації у вигляді словника
    transformation = [
                    {"width": 500, "height": 500, "crop": "fill"},
                    {"effect": "blur:300"},
                    {"quality": "auto"}
                ]

    # Завантаження фото з необхідними трансформаціями на Cloudinary
    uploaded_image = cloudinary.uploader.upload(
        file.file,
        folder="Webcore",
        transformation=transformation
    )

    # Збереження фото в базі даних з отриманими ID розміру та ефекту
    photo = Photo(
        filename=uploaded_image["public_id"],
        description=description,
        user_id=user_id,
        effect_id=effect.id,
        url=uploaded_image["url"]
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return photo_schema.Photo(**photo.__dict__)



# Iuliia 18.02.24 Видалення світлини (DELETE):
@router.delete("/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT, description="Видалення світлини")
async def delete_photo(photo_id: int, db: Session = Depends(database.get_db),
                       user: User = Depends(auth_service.get_current_user),
                       _: RoleAccess = Depends(allowed_operation_remove)):
    """
    Функція видаляє фотографію з бази даних і файлової системи.

    :param photo_id: int: ID фотографії, яку потрібно видалити
    :param db: Session: Доступ до бази даних
    :param user: User: Поточний користувач
    :param _: RoleAccess: Перевірка доступу користувача до цієї операції
    :return: HTTP статус код 204, що означає успішне виконання запиту
    """
    # Отримання фотографії з бази даних
    photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Видалення пов'язаних записів у таблиці image_links
    image_links = db.query(models.ImageLink).filter(models.ImageLink.photo_id == photo_id).all()
    for link in image_links:
        db.delete(link)
    db.commit()

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
    
    """
    The update_photo_handler function updates a photo in the database.
        The function takes as input:
            - photo_id: int, the id of the photo to be updated;
            - photo_data: PhotoUpdate, an object containing all fields that can be updated for a given user; 
                this is defined in schemas/photo.py and contains only non-nullable fields (i.e., no default values); 
                if any field is not provided by the user it will not be changed in the database;
            - db: Session = Depends(database.get_db),
    
    :param photo_id: int: Specify the photo id that will be updated
    :param photo_data: photo_schema.PhotoUpdate: Get the data from the request body
    :param db: Session: Get a database session
    :param user: User: Get the current user
    :param _: RoleAccess: Check if the user has permission to update a photo
    :return: A photo object
    :doc-author: Trelent
    """
    new_updated_photo = update_photo(db, photo_id, photo_data)     
    return new_updated_photo


# Iuliia 18.02.24 Отримання світлини за унікальним посиланням (GET):
@router.get("/photos/{photo_id}", status_code=status.HTTP_200_OK, description="Отримання світлини за унікальним посиланням")
def get_photo(photo_id: int, db: Session = Depends(database.get_db),
              user: User = Depends(auth_service.get_current_user),
              _: RoleAccess = Depends(allowed_operation_get)): #24/02/24 Olha
    
    """
    The get_photo function returns a photo object with the given id.
        If no photo is found, it raises an HTTP 404 error.
    
    
    :param photo_id: int: Specify the id of the photo to be retrieved
    :param db: Session: Pass the database session to the function
    :param user: User: Get the current user
    :param _: RoleAccess: Check if the user has access to this operation
    :return: The photo object from the database
    :doc-author: Trelent
    """
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
