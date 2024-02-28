from sqlalchemy.orm import Session
from src.db import models


def get_db():
    
    """
    The get_db function opens a new database connection if there is none yet for the current application context.
    It will also create the database tables if they don't exist yet.
    
    :return: A database connection
    :doc-author: Trelent
    """
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()
