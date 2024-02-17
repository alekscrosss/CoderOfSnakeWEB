from sqlalchemy.orm import Session
import models
import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    # Получаем пользователя по ид
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    # Получаем пользователя по имени
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    # Создаем пользователя, хешируем пароль, сохраняем в базу
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    # Получаем список пользователей
    return db.query(models.User).offset(skip).limit(limit).all()


def verify_password(plain_password, hashed_password):
    # Проверка на правильность пароля
    return pwd_context.verify(plain_password, hashed_password)
