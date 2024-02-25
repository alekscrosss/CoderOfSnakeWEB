# file scr\routers\tags.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas import tags_shemas
from src.schemas import photo_schema
from src.crud import tags

router = APIRouter()


@router.post("/photos/{photo_id}/tags", response_model=photo_schema.Photo)
def add_tags_to_photo(
    photo_id: int,
    tag_data: tags_shemas.PhotoTagsUpdate,
    db: Session = Depends(get_db)
):
    if len(tag_data.tags) > 5:
        raise HTTPException(status_code=400, detail="Cannot add more than 5 tags to a photo.")
    return tags.associate_tags_with_photo(db, photo_id, tag_data.tags)
