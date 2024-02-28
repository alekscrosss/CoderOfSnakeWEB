# file scr\crud\users.py

from sqlalchemy.orm import Session
from src.db.models import User
from src.schemas.user import UserModel


async def create_user(body: UserModel, db: Session):   
     
    """
    The create_user function creates a new user in the database.
        
    
    :param body: UserModel: Create a new user
    :param db: Session: Access the database
    :return: A user object
    :doc-author: Trelent
    """
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
     
    """
    The get_user_by_email function takes in an email and a database session,
        then returns the user with that email if it exists. If no such user exists,
        None is returned.
    
    :param email: str: Pass in the email address of the user
    :param db: Session: Create a session for the database
    :return: A user object or none
    :doc-author: Trelent
    """
    return  db.query(User).filter_by(email=email).first()



async def update_token(user: User, refresh_token, db: Session):
    
    """
    The update_token function updates the refresh_token for a user in the database.
        Args:
            user (User): The User object to update.
            refresh_token (str): The new refresh token to store in the database.
            db (Session): A connection to our Postgresql database.
    
    :param user: User: Identify the user that is logging in
    :param refresh_token: Update the refresh_token in the database
    :param db: Session: Pass the database session to the function
    :return: Nothing
    :doc-author: Trelent
    """
    user.refresh_token = refresh_token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    
    """
    The confirmed_email function takes in an email and a database session,
        then it gets the user by their email, sets their confirmed field to True,
        and commits the change to the database.
    
    :param email: str: Get the email of the user
    :param db: Session: Pass the database session to the function
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email,db)
    user.confirmed = True
    db.commit()

