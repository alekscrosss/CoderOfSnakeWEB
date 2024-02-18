# routes/photo.py
from fastapi import APIRouter, Depends, status, File, UploadFile
from sqlalchemy.orm import Session
import crud
import schemas
import database

router = APIRouter()


# Iuliia 18.02.24 Завантаження світлини з описом (POST):
@router.post("/photos/", status_code=status.HTTP_201_CREATED, description="Завантаження світлини з описом")
def create_photo(photo_data: schemas.PhotoCreate, file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    return crud.create_photo(db=db, photo_data=photo_data, file=file)


# Iuliia 18.02.24 Видалення світлини (DELETE):
@router.delete("/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT, description="Видалення світлини")
def delete_photo(photo_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_photo(db=db, photo_id=photo_id)


# Iuliia 18.02.24 Редагування опису світлини (PUT):
@router.put("/photos/{photo_id}", status_code=status.HTTP_200_OK, description="Редагування опису світлини")
def update_photo(photo_id: int, photo_data: schemas.PhotoUpdate, db: Session = Depends(database.get_db)):
    return crud.update_photo(db=db, photo_id=photo_id, photo_data=photo_data)


# Iuliia 18.02.24 Отримання світлини за унікальним посиланням (GET):
@router.get("/photos/{photo_id}", status_code=status.HTTP_200_OK, description="Отримання світлини за унікальним посиланням")
def get_photo(photo_id: int, db: Session = Depends(database.get_db)):
    return crud.get_photo(db=db, photo_id=photo_id)
