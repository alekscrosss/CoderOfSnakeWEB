import pytest
from unittest.mock import MagicMock, patch
from src.crud.users import get_user_by_email
from src.db.database import get_db
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.services.auth import Auth


@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_get_user_by_email():
    return MagicMock()

@pytest.fixture
def auth_service(mock_get_user_by_email, mock_db_session):
    return Auth()

def test_verify_password():
    auth = Auth()
    hashed_password = auth.get_password_hash("password")
    assert auth.verify_password("password", hashed_password) == True

def test_get_password_hash():
    auth = Auth()
    hashed_password = auth.get_password_hash("password")
    assert hashed_password is not None

def test_create_access_token(auth_service):
    data = {"sub": "test@example.com"}
    access_token = auth_service.create_access_token(data)
    assert access_token is not None

def test_create_refresh_token(auth_service):
    data = {"sub": "test@example.com"}
    refresh_token = auth_service.create_refresh_token(data)
    assert refresh_token is not None

# def test_get_current_user(auth_service, mock_db_session, mock_get_user_by_email):
#     token = "test_token"
#     mock_db_session.query().filter().first.return_value = None
#     with pytest.raises(HTTPException):
#         auth_service.get_current_user(token, mock_db_session)

def test_decode_refresh_token(auth_service):
    refresh_token = "test_token"
    decoded_email = auth_service.decode_refresh_token(refresh_token)
    assert decoded_email is not None

def test_create_email_token(auth_service):
    data = {"sub": "test@example.com"}
    email_token = auth_service.create_email_token(data)
    assert email_token is not None

# def test_get_email_from_token(auth_service):
#     token = "test_token"
#     email = auth_service.get_email_from_token(token)
#     assert email is not None
