import pytest

from unittest.mock import MagicMock
from sqlalchemy.orm import Session


from src.db.models import Comment
from src.crud.comment import create_comment, get_comments_by_photo_id, update_comment, delete_comment
from src.schemas.comment_schema import CommentCreate, CommentUpdate


@pytest.fixture
def mock_dataBase_session():
    return MagicMock(spec=Session)

def test_create_comment(mock_dataBase_session):
    comment_data = CommentCreate(content="To be or not to be")
    user_id = 1
    photo_id = 1

    created_comment = create_comment(mock_dataBase_session, 
                                     comment_data, user_id, 
                                     photo_id)
    
    assert isinstance(created_comment, Comment)
    assert created_comment.content == comment_data.content
    assert created_comment.user_id == user_id
    assert created_comment.photo_id == photo_id

def test_create_empty_comment(mock_dataBase_session):
    comment_data = CommentCreate(content="")
    user_id = 1
    photo_id = 1

    created_comment = create_comment(mock_dataBase_session, 
                                     comment_data, user_id, 
                                     photo_id)
    
    assert isinstance(created_comment, Comment)
    assert created_comment.content == "" or created_comment.content is None


def test_get_comments_by_photo_id(mock_dataBase_session):
    photo_id = 1  
    users_comments = [
        Comment(id=1, content="Test_comment_1", user_id=1, photo_id=photo_id),
        Comment(id=2, content="Test_comment_2", user_id=2, photo_id=photo_id)
    ] 

    mock_dataBase_session.query(Comment).filter(Comment.photo_id == photo_id).all.return_value = users_comments
    result = get_comments_by_photo_id(mock_dataBase_session, photo_id)
    assert result == users_comments

def test_update_comment(mock_dataBase_session):
    comment_id = 1
    user_id = 1

    comment_data = CommentUpdate(content="Appdated comment")
    mock_comment = Comment(id=comment_id, 
                           content="Last comment", 
                           user_id=user_id)
    mock_dataBase_session.query().filter().first.return_value = mock_comment
    
    updated_comment = update_comment(mock_dataBase_session, comment_id, comment_data, user_id)
    
    assert updated_comment.content == comment_data.content

def test_delete_comment(mock_dataBase_session):
    comment_id = 1
    user_id = 1

    mock_comment = Comment(id=comment_id, 
                           content="Test_comment_1", 
                           user_id=user_id)
    mock_dataBase_session.query().filter().first.return_value = mock_comment    
    deleted_comment = delete_comment(mock_dataBase_session, comment_id, user_id)    
    assert deleted_comment == mock_comment



