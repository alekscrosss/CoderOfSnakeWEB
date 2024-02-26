# routes/photo_cloud.py
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from src.services import cloudinary_service

router = APIRouter()

@router.post("/photos/", status_code=status.HTTP_201_CREATED, description="Завантаження світлини з описом")
async def create_photo(user_id: int, description: str = Form(...), file: UploadFile = File(...)):
    photo_url = cloudinary_service.upload_photo(file, description, user_id)
    return {"photo_url": photo_url}

@router.put("/photos/{photo_id}", status_code=status.HTTP_200_OK, description="Редагування світлини")
async def update_photo(photo_id: int, file: UploadFile = File(...)):
    photo_url = cloudinary_service.update_photo(photo_id, file)
    return {"photo_url": photo_url}
