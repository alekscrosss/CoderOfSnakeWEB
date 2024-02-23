from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.db.models import Comment
from src.schemas.comment_schema import CommentCreate, CommentUpdate

from passlib.context import CryptContext

def create_comment(db: Session, comment: CommentCreate, user_id: int, photo_id: int):
    db_comment = Comment(content=comment.content, user_id=user_id, photo_id=photo_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_photo_id(db: Session, photo_id: int):
    return db.query(Comment).filter(Comment.photo_id == photo_id).all()

def update_comment(db: Session, comment_id: int, comment: CommentUpdate, user_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        return None
    if db_comment.user_id != user_id:
        raise HTTPException(status_code=400, detail="Not allowed to edit this comment")
    for var, value in vars(comment).items():
        setattr(db_comment, var, value) if value is not None else None
    db_comment.updated_at = func.now()
    db.commit()
    return db_comment

def delete_comment(db: Session, comment_id: int, user_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        return None
    db.delete(db_comment)
    db.commit()
    return db_comment