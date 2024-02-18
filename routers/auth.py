from typing import List

from fastapi import Depends, HTTPException, status, APIRouter, Security, BackgroundTasks, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserModel, UserResponse, TokenModel, RequestEmail #check
#from src.repository import users as repository_users
from scripts import users_auth
from services.auth import auth_service
from services.email import send_email
from fastapi_limiter.depends import RateLimiter
from conf import messages
import crud
router = APIRouter(prefix="/auth", tags=['auth'])
security = HTTPBearer()


# Обмежуйте кількість запитів до своїх маршрутів контактів. Обов’язково обмежте швидкість - створення контактів для користувача;
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED             )
async def signup(body: UserModel, background_task: BackgroundTasks, request: Request, db: Session = Depends(get_db)):

    exist_user = await crud.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=messages.EMAIL_NOT_CONFIRMED)
    body.password = auth_service.get_password_hash(body.password)
    new_user = await crud.create_user(body, db)
    background_task.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = await crud.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_PASSWORD)
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.EMAIL_NOT_CONFIRMED)
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_PASSWORD)
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await users_auth.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):

    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await crud.get_user_by_email(email, db)
    if user.refresh_token != token:
        await users_auth.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_REFRESH_TOKEN)

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await users_auth.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):

    email = auth_service.get_email_from_token(token)
    user = await crud.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.VERIFICATION_ERROR)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await users_auth.confirmed_email(email, db)
    return {"message": "Email was confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_task: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):

    user = await crud.get_user_by_email(body.email, db)
    if user and user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_task.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": "Check your email for confirmation"}
