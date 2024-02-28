import pytest
from unittest.mock import MagicMock, patch
from src.crud.photo import create_photo
from src.crud.photo import delete_photo, update_photo, get_photo
from src.db.models import Photo
from sqlalchemy.orm import Session
from fastapi import HTTPException



@pytest.fixture
def mock_database_session():
    return MagicMock(spec=Session)


def test_create_photo(mock_database_session):
    user_id = 1
    description = "Test description"
    size = None
    effect = None
    file_mock = MagicMock()  # Створюємо мок для об'єкту UploadFile

    # Мокуємо функцію cloudinary.uploader.upload
    with patch("src.crud.photo.cloudinary.uploader.upload") as upload_mock:
        # Повертаємо макетований об'єкт, як результат виклику cloudinary.uploader.upload
        upload_mock.return_value = {"public_id": "mocked_public_id"}

        # Викликаємо функцію create_photo з моками
        created_photo = create_photo(user_id, description, size, effect, file=file_mock, db=mock_database_session)

    # Перевіряємо, чи була викликана функція cloudinary.uploader.upload з правильними параметрами
    upload_mock.assert_called_once_with(file_mock.file, folder="Webcore")

    # Перевіряємо, чи було викликано метод add на об'єкті сеансу бази даних з правильним параметром
    mock_database_session.add.assert_called_once()

    # Отримуємо об'єкт Photo, який був переданий у метод add
    added_photo = mock_database_session.add.call_args[0][0]

    # Перевіряємо, що це об'єкт класу Photo
    assert isinstance(added_photo, Photo)

    # Перевіряємо, що об'єкт Photo має очікувані атрибу


def test_delete_photo(mock_database_session):
    # Створення моку для фото, яке буде знайдено в базі даних
    photo = Photo(id=1, filename="test.jpg")

    # Мокування запиту до бази даних, щоб повернути фото
    mock_database_session.query().filter().first.return_value = photo

    # Виклик функції видалення фото
    assert delete_photo(1, mock_database_session) == True

    # Перевірка, чи викликався метод видалення на об'єкті сеансу бази даних з правильним параметром
    mock_database_session.delete.assert_called_once_with(photo)


def test_delete_photo_not_found(mock_database_session):
    photo_id = 1
    mock_database_session.query().filter().first.return_value = None
    assert delete_photo(photo_id, mock_database_session) == False


def test_update_photo(mock_database_session):
    photo_id = 1
    description = "New description"
    photo_data = MagicMock()
    photo_data.description = description
    photo = Photo(id=photo_id, description="Old description")
    mock_database_session.query().filter().first.return_value = photo
    updated_photo = update_photo(mock_database_session, photo_id, photo_data)
    assert updated_photo.description == description
    mock_database_session.commit.assert_called_once()
    mock_database_session.refresh.assert_called_once_with(photo)


def test_update_photo_not_found(mock_database_session):
    photo_id = 1
    photo_data = MagicMock()
    photo_data.description = "New description"
    mock_database_session.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        update_photo(mock_database_session, photo_id, photo_data)
    assert exc_info.value.status_code == 404


def test_get_photo(mock_database_session):
    photo_id = 1
    photo = Photo(id=photo_id)
    mock_database_session.query().filter().first.return_value = photo
    assert get_photo(mock_database_session, photo_id) == photo
