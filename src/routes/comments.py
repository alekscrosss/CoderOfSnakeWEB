# file routers/comments.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.services.auth import auth_service
from src.db.database import get_db
from src.schemas.comment_schema import CommentCreate, CommentUpdate, Comment, User
from src.services.roles import RoleAccess #24/02/2024 Olha 
from src.db.models import Role, User #24/02/2024 Olha

from src.crud.comment import create_comment, get_comments_by_photo_id, update_comment, delete_comment


router = APIRouter()

#24/02/2024 Olha
allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_remove = RoleAccess([Role.admin, Role.moderator])

@router.post("/photos/{photo_id}/comments/", response_model=Comment)
def create_comment_for_photo(
    photo_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
    _: RoleAccess = Depends(allowed_operation_create) #24/02/2024 Olha
):
    return create_comment(db=db, comment=comment, user_id=current_user.id, photo_id=photo_id)


@router.get("/photos/{photo_id}/comments/", response_model=List[Comment])
def read_comments_for_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    _: RoleAccess = Depends(allowed_operation_get) #24/02/2024 Olha
):
    return get_comments_by_photo_id(db=db, photo_id=photo_id)


@router.patch("/comments/{comment_id}/", response_model=Comment)
def update_comment_handler(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
    _: RoleAccess = Depends(allowed_operation_update) #24/02/2024 Olha
):
    return update_comment(db=db, comment_id=comment_id, comment=comment, user_id=current_user.id)


@router.delete("/comments/{comment_id}/")
def delete_comment_handler(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
    _: RoleAccess = Depends(allowed_operation_remove) #24/02/2024 Olha
):
    delete_comment(db=db, comment_id=comment_id, user_id=current_user.id)
    return {"detail": "Comment deleted"}