from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud
import schemas
import database

router = APIRouter()
from conf import messages #18/02/2024 Olha

# Создаем пользователя
@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail=messages.ACCOUNT_ALREADY_EXISTS) #18/02/2024 Olha
    return crud.create_user(db=db, user=user)
