from sqlalchemy.orm import Session
import models


def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()