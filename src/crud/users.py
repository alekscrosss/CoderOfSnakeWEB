from sqlalchemy.orm import Session
from src.db.models import User
from src.schemas.user import UserModel


async def create_user(body: UserModel, db: Session):    
    admin_exists = db.query(User).filter(User.role == 'admin').first()
    if admin_exists:
        new_user = User(**body.dict(), role='user')
    else:
        new_user = User(**body.dict(),  role='admin')
    #new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def get_user_by_email(email: str, db: Session) -> User | None:    
    return  db.query(User).filter_by(email=email).first()



async def update_token(user: User, refresh_token, db: Session):
    user.refresh_token = refresh_token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email,db)
    user.confirmed = True
    db.commit()

