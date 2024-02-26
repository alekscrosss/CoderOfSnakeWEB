# services/cloudinary_service.py
import cloudinary.uploader
from fastapi import UploadFile


def upload_photo(file: UploadFile, description: str, user_id: int) -> str:
    uploaded_image = cloudinary.uploader.upload(file.file,
                                                folder="Webcore",
                                                transformation=[
                                                    {"width": 500, "height": 500, "crop": "fill"},
                                                    {"effect": "grayscale"},
                                                    {"quality": "auto"}
                                                ])
    return uploaded_image["secure_url"]

def update_photo(photo_id: int, file: UploadFile) -> str:
    # Логіка оновлення фото в Cloudinary
    pass
