from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from src.db.models import Comment, User
from src.db.database import get_db
from src.crud.comment import create_comment, delete_comment, get_comments_by_photo_id, update_comment

client = TestClient(app)

def test_create_comment(session: Session, user: User, photo_id: int):
    # Предполагаем, что `user` и `photo_id` уже созданы и доступны
    response = client.post(
        f"/photos/{photo_id}/comments/",
        json={"content": "Great photo!"},
        headers={"Authorization": f"Bearer {user.access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Great photo!"
    assert data["user_id"] == user.id
    assert data["photo_id"] == photo_id

def test_read_comments(session: Session, photo_id: int, user_id: int):
    # Создание комментария перед чтением всех комментариев к фотографии
    create_comment(session, "Nice shot!", user_id, photo_id)
    response = client.get(f"/photos/{photo_id}/comments/")
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0

def test_update_comment(session: Session, user: User, comment_id: int):
    response = client.patch(
        f"/comments/{comment_id}/",
        json={"content": "Updated comment"},
        headers={"Authorization": f"Bearer {user.access_token}"}
    )
    assert response.status_code == 200
    updated_comment = response.json()
    assert updated_comment["content"] == "Updated comment"

def test_delete_comment(session: Session, user: User, comment_id: int):
    response = client.delete(
        f"/comments/{comment_id}/",
        headers={"Authorization": f"Bearer {user.access_token}"}
    )
    assert response.status_code == 200
    # Проверяем, что комментарий был удален
    db_comment = session.query(Comment).filter(Comment.id == comment_id).first()
    assert db_comment is None
