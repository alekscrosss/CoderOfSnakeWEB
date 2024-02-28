# file scr\crud\tags.py

from sqlalchemy.orm import Session
from src.db import models
from src.schemas import tags_shemas
from typing import List


def get_tag_by_name(db: Session, name: str):
    
    """
    The get_tag_by_name function returns the tag with the given name.
        
        Args:
            db (Session): The database session to use for querying.
            name (str): The name of the tag to retrieve from the database.
    
    :param db: Session: Pass the database session to the function
    :param name: str: Filter the database by name
    :return: A tag object with the given name
    :doc-author: Trelent
    """
    return db.query(models.Tag).filter(models.Tag.name == name).first()


def create_tag(db: Session, tag: tags_shemas.TagCreate):
    
    """
    The create_tag function creates a new tag in the database.
        Args:
            db (Session): The database session to use for creating the tag.
            tag (TagCreate): The data of the new tag to create.
        Returns:
            Tag: A newly created Tag object with its ID populated from the database.
    
    :param db: Session: Pass the database session to the function
    :param tag: tags_shemas.TagCreate: Create a new tag
    :return: A tag object
    :doc-author: Trelent
    """
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def associate_tags_with_photo(db: Session, photo_id: int, tag_names: List[str]):
    
    """
    The associate_tags_with_photo function takes a photo_id and a list of tag names.
    It then associates the tags with the photo, creating new tags if necessary.
    
    :param db: Session: Pass in the database session
    :param photo_id: int: Identify the photo to associate tags with
    :param tag_names: List[str]: Pass in a list of tag names to associate with the photo
    :return: A photo object, but the response is a list of tags
    :doc-author: Trelent
    """
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
