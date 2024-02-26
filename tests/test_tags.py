from src.db import models

def test_create_tag(client, session):
    tag_data = {"name": "Nature"}
    response = client.post("/tags/", json=tag_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == tag_data["name"]
    db_tag = session.query(models.Tag).filter(models.Tag.name == tag_data["name"]).first()
    assert db_tag is not None
    assert db_tag.name == tag_data["name"]

def test_get_tag_by_name(client, session):
    response = client.get(f"/tags/Nature")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Nature"
    db_tag = session.query(models.Tag).filter(models.Tag.name == "Nature").first()
    assert db_tag is not None
    assert db_tag.name == "Nature"

def test_associate_tags_with_photo(client, session):
    photo_id = 1
    tag_names = ["Nature", "Landscape"]
    for tag_name in tag_names:
        session.merge(models.Tag(name=tag_name))
    session.commit()
    response = client.post(f"/photos/{photo_id}/tags", json={"tags": tag_names})
    assert response.status_code == 200
    db_photo = session.query(models.Photo).filter(models.Photo.id == photo_id).first()
    assert db_photo is not None
    assert len(db_photo.tags) == len(tag_names)
    for tag in db_photo.tags:
        assert tag.name in tag_names
