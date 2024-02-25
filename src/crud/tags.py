# file scr\crud\tags.py

from sqlalchemy.orm import Session
from src.db import models
from src.schemas import tags_shemas
from typing import List


def get_tag_by_name(db: Session, name: str):
    return db.query(models.Tag).filter(models.Tag.name == name).first()


def create_tag(db: Session, tag: tags_shemas.TagCreate):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def associate_tags_with_photo(db: Session, photo_id: int, tag_names: List[str]):
    tags_to_associate = []
    for tag_name in tag_names:
        tag = get_tag_by_name(db, tag_name)
        if not tag:
            tag = create_tag(db, tags_shemas.TagCreate(name=tag_name))
        tags_to_associate.append(tag)

    photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if photo:
        for tag in tags_to_associate:
            if tag not in photo.tags:
                photo.tags.append(tag)
        db.commit()
    return photo
