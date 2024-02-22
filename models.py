# file models.py

from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table, DateTime, Boolean, Enum, func #18/02/2024 Olha
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


from datetime import datetime

import enum #18/02/2024 Olha
import os

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost/db2"
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


# Iuliia 18.02.24
class Photo(Base):
    # Модель для зберігання фотографій користувачів

    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    # Зв'язок з користувачем
    user = relationship("User", backref="photos") #18/02/2024 Olha fix create user


 # Nazar 22.02.24
 class Tag(Base):
     tablename = 'tags'

     id = Column(Integer, primary_key=True, index=True)
     name = Column(String, unique=True, index=True)


 image_tag_association = Table('image_tag_association', Base.metadata,
     Column('image_id', Integer, ForeignKey('images.id')),
     Column('tag_id', Integer, ForeignKey('tags.id'))
 )


class Comment(Base):
    # Модель коментариев..
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    photo_id = Column(Integer, ForeignKey("photos.id"))

    user = relationship("User", backref="comments")
    photo = relationship("Photo", backref="comments")

