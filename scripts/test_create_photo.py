import io
from fastapi import UploadFile

from src.crud.photo import create_photo
from src.crud.tags import create_tag
from src.db.models import SessionLocal


# ...

def test_create_photo_with_tag():
    # Підготовка тестового середовища
    db = SessionLocal()
    tag_name = "tree"
    tag = create_tag(db, name=tag_name)

    # Виклик функції, яку потрібно протестувати
    filename = "flower.jpg"
    description = "good"
    user_id = 1
    tag_id = tag.id
    file_content = b"E:\\PYTHON\\Team_project_2\\images\\flower.jpg"  # Вміст файлу, який ви хочете завантажити
    file = UploadFile(filename=filename, file=io.BytesIO(file_content))
    photo = create_photo(db, filename, user_id, file, description, tag_id)


    # Перевірка результатів
    assert photo.filename == filename
    assert photo.description == description
    assert photo.user_id == user_id
    assert tag_id in [tag.id for tag in photo.tags]
