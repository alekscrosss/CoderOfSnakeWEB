from sqlalchemy.orm import Session
from src.db import models


def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()
