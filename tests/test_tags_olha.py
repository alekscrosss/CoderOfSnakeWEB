import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.db.models import Tag

from src.crud.tags import get_tag_by_name, create_tag, associate_tags_with_photo
from src.schemas.tags_shemas import TagCreate


@pytest.fixture
def mock_dataBase_session():
    return MagicMock(spec=Session)

def test_create_tag(mock_dataBase_session):
    data_tag = TagCreate(name="Nature")
    created_tag = create_tag(mock_dataBase_session, data_tag)
    
    assert isinstance(created_tag, Tag)
    assert created_tag.name == data_tag.name


def test_get_tag_by_name(mock_dataBase_session):
    tag_name = "Nature"
    tag = Tag(id=1, name=tag_name)
    mock_dataBase_session.query(Tag).filter(Tag.name == tag_name).first.return_value = tag    
    result = get_tag_by_name(mock_dataBase_session, tag_name)
    
    assert result == tag





