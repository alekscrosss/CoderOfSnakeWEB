# file scr\crud\comment.py

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.db.models import Comment
from src.schemas.comment_schema import CommentCreate, CommentUpdate

from passlib.context import CryptContext

def create_comment(db: Session, comment: CommentCreate, user_id: int, photo_id: int):
    
    """
    The create_comment function creates a new comment in the database.
        Args:
            db (Session): The database session object.
            comment (CommentCreate): The CommentCreate object to be created in the database.
            user_id (int): The id of the user who is creating this comment.
            photo_id (int): The id of the photo that this comment is being made on.
    
    :param db: Session: Connect to the database
    :param comment: CommentCreate: Pass the comment data to the function
    :param user_id: int: Identify the user who created the comment
    :param photo_id: int: Identify which photo the comment is for
    :return: The newly created comment
    :doc-author: Trelent
    """
    db_comment = Comment(content=comment.content, user_id=user_id, photo_id=photo_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_photo_id(db: Session, photo_id: int):
    
    """
    The get_comments_by_photo_id function returns all comments associated with a given photo_id.
        Args:
            db (Session): The database session to use for querying the database.
            photo_id (int): The id of the photo whose comments are being retrieved.
        Returns:
            List[Comment]: A list of Comment objects that correspond to the given photo_id.
    
    :param db: Session: Pass the database session into the function
    :param photo_id: int: Filter the comments by photo_id
    :return: A list of comment objects
    :doc-author: Trelent
    """
    return db.query(Comment).filter(Comment.photo_id == photo_id).all()

def update_comment(db: Session, comment_id: int, comment: CommentUpdate, user_id: int):
    
    """
    The update_comment function updates a comment in the database.
        Args:
            db (Session): The database session to use for updating the comment.
            comment_id (int): The id of the comment to update.
            user_id (int): The id of the user who is making this request, used for authorization purposes.
        Returns: 
            CommentUpdate: An updated version of the original Comment object.
    
    :param db: Session: Pass the database session to the function
    :param comment_id: int: Find the comment in the database
    :param comment: CommentUpdate: Update the comment
    :param user_id: int: Check if the user is allowed to edit the comment
    :return: A comment object
    :doc-author: Trelent
    """
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
    
    """
    The delete_comment function deletes a comment from the database.
        Args:
            db (Session): The database session object.
            comment_id (int): The id of the comment to be deleted.
            user_id (int): The id of the user who is deleting this comment.
    
    :param db: Session: Pass the database session to the function
    :param comment_id: int: Find the comment in the database
    :param user_id: int: Check if the user is authorized to delete the comment
    :return: The comment that was deleted
    :doc-author: Trelent
    """
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        return None
    db.delete(db_comment)
    db.commit()
    return db_comment