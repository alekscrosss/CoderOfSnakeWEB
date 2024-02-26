import pytest
from unittest.mock import MagicMock, AsyncMock
from src.db.models import User
from src.crud.users import create_user, get_user_by_email, update_token


#26/02/2024 Olha
@pytest.mark.asyncio
async def test_create_new_user_with_exists_admin():
    db_mock = MagicMock()
    admin_exists_query_mock = AsyncMock(return_value=True)
    db_mock.query.return_value.filter.return_value.first.return_value = True

    data = MagicMock()
    data.dict.return_value = {
        "username": "dev_user", 
        "email": "dev_user@gmail.com", 
        "password": "qwerty"
        }
    new_user = await create_user(data, db_mock)
    assert new_user.role == 'user'


@pytest.mark.asyncio
async def test_create_new_user_without_admin_exists():
    db_mock = MagicMock()
    admin_not_exists_query_mock = AsyncMock(return_value=False)
    db_mock.query.return_value.filter.return_value.first.return_value = False

    data = MagicMock()
    data.dict.return_value = {
        "username": "dev_user", 
        "email": "dev_user@gmail.com", 
        "password": "qwerty"
        }

    new_user = await create_user(data, db_mock)
    assert new_user.role == 'admin'

def test_get_user_by_email():
    db_mock = MagicMock()
    user_query_mock = AsyncMock(return_value=User(email="dev_user@gmail.com"))
    db_mock.query.return_value.filter_by.return_value.first = user_query_mock
    user = get_user_by_email("dev_user@gmail.com", db_mock)

    assert user is not None

@pytest.mark.asyncio
async def test_update_token():
    db_mock = MagicMock()
    user = User()
    await update_token(user, "new_refresh_token", db_mock)

    assert user.refresh_token == "new_refresh_token"

