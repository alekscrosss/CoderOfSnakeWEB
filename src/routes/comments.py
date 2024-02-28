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
    
    """
    The create_comment_for_photo function creates a comment for a photo.
        The function takes the following parameters:
            - photo_id: int, the id of the photo to which we want to add a comment;
            - comment: CommentCreate, an object containing all information needed to create a new Comment;
            - db: Session = Depends(get_db), an SQLAlchemy session that will be used by this function;
            - current_user: User = Depends(auth_service.get_current_user), an object representing the user who is currently logged in and making this request (this
    
    :param photo_id: int: Get the photo id from the url
    :param comment: CommentCreate: Create a new comment
    :param db: Session: Access the database
    :param current_user: User: Get the current user
    :param _: RoleAccess: Check if the user has permission to create a comment
    :return: A comment object
    :doc-author: Trelent
    """
    return create_comment(db=db, comment=comment, user_id=current_user.id, photo_id=photo_id)


@router.get("/photos/{photo_id}/comments/", response_model=List[Comment])
def read_comments_for_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    _: RoleAccess = Depends(allowed_operation_get) #24/02/2024 Olha
):
    
    """
    The read_comments_for_photo function returns a list of comments for the photo with the given ID.
        The function takes in an integer representing a photo ID and returns a list of comment objects.
    
    :param photo_id: int: Specify the photo id for which we want to retrieve comments
    :param db: Session: Pass the database session to the function
    :param _: RoleAccess: Check if the user has access to this endpoint
    :return: The comments for a photo
    :doc-author: Trelent
    """
    return get_comments_by_photo_id(db=db, photo_id=photo_id)


@router.patch("/comments/{comment_id}/", response_model=Comment)
def update_comment_handler(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
    _: RoleAccess = Depends(allowed_operation_update) #24/02/2024 Olha
):
    
    """
    The update_comment_handler function updates a comment in the database.
        The function takes three arguments:
            - db: A Session object that is used to query the database.
            - comment_id: An integer representing the id of a Comment object in the database.  This argument is required and must be an integer greater than 0 (zero).  If this argument is not provided, or if it does not meet these requirements, then an HTTP 400 error will be returned to indicate that there was a problem with your request parameters.  
        - comment: A CommentUpdate object containing information about how you want to update your existing Comment object in
    
    :param comment_id: int: Identify the comment to be updated
    :param comment: CommentUpdate: Get the comment data from the request body
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user information
    :param _: RoleAccess: Check if the user has permission to update a comment
    :return: A comment object
    :doc-author: Trelent
    """
    return update_comment(db=db, comment_id=comment_id, comment=comment, user_id=current_user.id)


@router.delete("/comments/{comment_id}/")
def delete_comment_handler(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
    _: RoleAccess = Depends(allowed_operation_remove) #24/02/2024 Olha
):
    
    """
    The delete_comment_handler function deletes a comment from the database.
        The function takes in an integer representing the id of the comment to be deleted,
        and returns a JSON object containing a detail message indicating that 
        &quot;Comment deleted&quot; if successful.
    
    :param comment_id: int: Specify the id of the comment that is going to be deleted
    :param db: Session: Get access to the database
    :param current_user: User: Get the user that is currently logged in
    :param _: RoleAccess: Check if the user has permission to perform this operation
    :return: A dict with the message &quot;comment deleted&quot;
    :doc-author: Trelent
    """
    delete_comment(db=db, comment_id=comment_id, user_id=current_user.id)
    return {"detail": "Comment deleted"}