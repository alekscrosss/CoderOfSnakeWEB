# file models.py
import os
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table, DateTime, Boolean, Enum, func #18/02/2024 Olha
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

import enum #18/02/2024 Olha
from dotenv import load_dotenv
load_dotenv()


SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Role(enum.Enum): #18/02/2024 Olha
    user: str = 'user'
    admin: str = 'admin'
    moderator: str = 'moderator'    


class User(Base): #18/02/2024 Olha
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    email = Column(String(100), nullable=False, unique=True) #nullable=False - не може бути пустим
    password = Column(String(100), nullable=False)    
    refresh_token = Column(String(255), nullable=True)
    role = Column('role', Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False) #при першій реєстрації юзер не підтверджений
    status_ban = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now()) # дата та час створення
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now()) # дата та час оновлення данних

    photos = relationship("Photo", back_populates="user")
    comments = relationship("Comment", back_populates="user")


# Iuliia 18.02.24
class Photo(Base):
    # Модель для зберігання фотографій користувачів

    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    size_id = Column(Integer, ForeignKey("sizes.id"), index=True, nullable=True)
    effect_id = Column(Integer, ForeignKey("effects.id"), index=True, nullable=True)
    url = Column(String, index=True)

    # Зв'язок з користувачем
    user = relationship("User", back_populates="photos")
    comments = relationship("Comment", back_populates="photo")
    tags = relationship("Tag", secondary="photo_tag_association", back_populates="photos")
    image_links = relationship("ImageLink", back_populates="photo")
    size = relationship("Size")  # Додайте зв'язок з моделлю Size
    effect = relationship("Effect")  # Додайте зв'язок з моделлю Effect

class Size(Base):
    __tablename__ = "sizes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    width = Column(Integer)
    height = Column(Integer)

    photos = relationship("Photo", back_populates="size")


class Effect(Base):
    __tablename__ = "effects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)  # Додали поле опису

    photos = relationship("Photo", back_populates="effect")


class Comment(Base):
    # Модель коментариев..
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    photo_id = Column(Integer, ForeignKey("photos.id"))

    user = relationship("User", back_populates="comments")
    photo = relationship("Photo", back_populates="comments")


photo_tag_association = Table(
    'photo_tag_association', Base.metadata,
    Column('photo_id', Integer, ForeignKey('photos.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    photos = relationship("Photo", secondary="photo_tag_association", back_populates="tags")


class ImageLink(Base):
    __tablename__ = "image_links"

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey('photos.id'), nullable=False)
    url = Column(String, nullable=False)
    qr_code = Column(String, nullable=True)  # Путь к файлу QR-кода

    photo = relationship("Photo", back_populates="image_links")