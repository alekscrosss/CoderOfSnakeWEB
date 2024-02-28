import pytest
from pydantic import ValidationError
from src.schemas.photo_schema import PhotoBase, PhotoCreate, PhotoUpdate, Photo

def test_photo_base():
    filename = "test.jpg"
    photo_base = PhotoBase(filename=filename)
    assert photo_base.filename == filename

def test_photo_create():
    filename = "test.jpg"
    description = "Test photo"
    size_id = 1
    size = None
    effect = None

    # Перевірка створення за допомогою alias
    photo_create = PhotoCreate(filename=filename, description=description, size=size, effect=effect, size_id=size_id)
    assert photo_create.filename == filename
    assert photo_create.description == description
    assert photo_create.size == size
    assert photo_create.effect == effect
    assert photo_create.size_id == size_id

def test_photo_update():
    description = "Updated description"
    photo_update = PhotoUpdate(description=description)
    assert photo_update.description == description

def test_photo_model():
    filename = "test.jpg"
    description = "Test photo"
    user_id = 1
    photo_id = 1

    # Перевірка створення за допомогою alias
    photo = Photo(filename=filename, description=description, user_id=user_id, id=photo_id)
    assert photo.filename == filename
    assert photo.description == description
    assert photo.user_id == user_id
    assert photo.id == photo_id
