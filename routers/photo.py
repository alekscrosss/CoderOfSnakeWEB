from fastapi import APIRouter, Depends, status, File, UploadFile
from sqlalchemy.orm import Session
import crud
import schemas
import database

router = APIRouter()


@router.post("/photos/", status_code=status.HTTP_201_CREATED)
def create_photo(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
  # Заглушка
    return {"filename": file.filename}
