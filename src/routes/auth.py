# file routers/comments.py
from typing import List

from fastapi import Depends, HTTPException, status,  APIRouter,  Security, BackgroundTasks, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.user import UserModel, UserResponse, TokenModel, RequestEmail
from src. crud import users as repository_users
from src.services.auth import auth_service
from src.services.email import send_email

from fastapi import FastAPI #13

from ipaddress import ip_address #13
from typing import Callable #13
from fastapi.responses import JSONResponse #13

router = APIRouter(prefix="/auth", tags=['auth'])
security = HTTPBearer()

app = FastAPI() 


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    
    """
    The signup function creates a new user in the database.
        It also sends an email to the user with a link to verify their account.
        The function returns the newly created UserModel object.
    
    :param body: UserModel: Get the data from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background queue
    :param request: Request: Get the base_url of the application
    :param db: Session: Get the database session
    :return: A user object
    :doc-author: Trelent
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    """
    The login function is used to authenticate a user.
    
    :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
    :param db: Session: Access the database
    :return: A dict with the access_token and refresh_token
    :doc-author: Trelent
    """
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    #якщо емейл не підтверджений  нас не пусте залогіниться
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    
    """
    The refresh_token function is used to refresh the access token.
        The function takes in a refresh token and returns an access_token, 
        a new refresh_token, and the type of token (bearer).
    
    :param credentials: HTTPAuthorizationCredentials: Get the token from the request header
    :param db: Session: Get the database session
    :return: A dictionary with the access_token and refresh_token
    :doc-author: Trelent
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    
    """
    The confirmed_email function is used to confirm a user's email address.
        It takes the token from the URL and uses it to get the user's email address.
        Then, it checks if that user exists in our database and if they have already confirmed their email.
        If not, then we update their record in our database with a confirmation of their email.
    
    :param token: str: Get the token from the url
    :param db: Session: Get the database session
    :return: The message &quot;email confirmed&quot;
    :doc-author: Trelent
    """
    email =  auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}

@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    
    """
    The request_email function is used to send an email to the user with a link that will allow them
    to confirm their email address. The function takes in a RequestEmail object, which contains the 
    user's email address. It then checks if there is already a user with that email address in the database, and if so, whether or not they have confirmed their account yet. If they have not confirmed it yet, it sends an email containing a confirmation link using FastAPI's BackgroundTasks feature.
    
    :param body: RequestEmail: Get the email from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks
    :param request: Request: Get the base url of the server
    :param db: Session: Access the database
    :return: A message
    :doc-author: Trelent
    """
    user = await repository_users.get_user_by_email(body.email, db)

    if user and user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": "Check your email for confirmation."}