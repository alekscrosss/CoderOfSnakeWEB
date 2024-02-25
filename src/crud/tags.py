# # crud/tags.py
# from sqlalchemy.orm import Session
# from src.db.models import Photo, Tag
# from fastapi import HTTPException
#
# def create_tag(db: Session, name: str):
#     # Створюємо новий тег
#     tag = Tag(name=name)
#     db.add(tag)
#     db.commit()
#     db.refresh(tag)
#     return tag
#
# def add_tags_to_photo(db: Session, photo_id: int, tags: list):
#     # Отримуємо фотографію з бази даних
#     photo = db.query(Photo).filter(Photo.id == photo_id).first()
#     if not photo:
#         raise HTTPException(status_code=404, detail="Photo not found")
#
#     # Додаємо теги до фотографії
#     tag_ids = []
#     for tag_name in tags:
#         tag = db.query(Tag).filter(Tag.name == tag_name).first()
#         if not tag:
#             tag = Tag(name=tag_name)
#             db.add(tag)
#             db.commit()
#             db.refresh(tag)
#         tag_ids.append(tag.id)
#
#     # Додаємо теги до фотографії
#     photo.tags.extend(tag_ids)
#     db.commit()
#     db.refresh(photo)
#
#     return {"message": "Tags added successfully"}
