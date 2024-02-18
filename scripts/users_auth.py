from sqlalchemy.orm import Session
from models import User
from schemas import UserModel

from crud import get_user_by_email

async def update_token(user: User, refresh_token, db: Session):
    user.refresh_token = refresh_token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
