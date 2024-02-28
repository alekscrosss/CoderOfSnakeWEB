import pickle #cash
from datetime import datetime, timedelta
from typing import Optional
import os
import redis #cash
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer  
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.db.database import get_db
from src.crud import users as repository_users
from dotenv import load_dotenv
load_dotenv()


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    SECRET_KEY = os.environ.get('SECRET_KEY')
    ALGORITHM = os.environ.get('ALGORITHM')
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS'), db=0) #cash

    def verify_password(self, plain_password, hashed_password):
        
        """
        The verify_password function takes a plain-text password and the hashed version of that password,
            and returns True if they match, False otherwise.
        
        
        :param self: Make the method a bound method, which means that it can be called on an instance of the class
        :param plain_password: Compare the password that is entered with the hashed_password parameter
        :param hashed_password: Compare the hashed password in the database with the plain_password entered by user
        :return: A boolean value
        :doc-author: Trelent
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        
        """
        The get_password_hash function takes a password as an argument and returns the hash of that password.
            The function uses the pwd_context object to generate a hash from the given password.
        
        :param self: Represent the instance of the class
        :param password: str: Pass the password to be hashed into the function
        :return: A hash of the password
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)


    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        
        """
        The create_access_token function creates a new access token for the user.
            
        
        :param self: Represent the instance of the class
        :param data: dict: Pass the data to be encoded
        :param expires_delta: Optional[float]: Specify the expiration time of the token
        :return: An encoded access token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token


# define a function to generate a new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        
        """
        The create_refresh_token function creates a refresh token for the user.
            Args:
                data (dict): A dictionary containing the user's id and username.
                expires_delta (Optional[float]): The number of seconds until the refresh token expires. Defaults to None, which sets it to 7 days from now.
        
        :param self: Represent the instance of the class
        :param data: dict: Pass the user's data to the function
        :param expires_delta: Optional[float]: Set the expiration time for the refresh token
        :return: An encoded refresh token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token


    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        
        """
        The get_current_user function is a dependency that will be called by FastAPI to retrieve the current user.
        It uses the token retrieved from the Authorization header and decodes it using PyJWT. If successful, it returns
        the user object associated with that email address.
        
        :param self: Represent the instance of a class
        :param token: str: Get the token from the request header
        :param db: Session: Pass the database connection to the function
        :return: A user object
        :doc-author: Trelent
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == "access_token":
                email = payload.get("sub")
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception       


        user = self.r.get(f"user:{email}")
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.r.set(f"user:{email}", pickle.dumps(user))
            self.r.expire(f"user:{email}", 900)
        else:
            user = pickle.loads(user)
        
        #cach end
        if user is None:
            raise credentials_exception
        return user


    async def decode_refresh_token(self, refresh_token: str):
        
        """
        The decode_refresh_token function takes a refresh token and decodes it.
            If the scope is 'refresh_token', then we return the email address of the user.
            Otherwise, we raise an HTTPException with status code 401 (UNAUTHORIZED) and detail message 'Invalid scope for token'.
        
        
        :param self: Represent the instance of the class
        :param refresh_token: str: Pass the refresh token to the function
        :return: A string
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    def create_email_token(self, data: dict):
        
        """
        The create_email_token function creates a token that is used to verify the user's email address.
            The token contains the following data:
                - iat (issued at): The time when the token was created.
                - exp (expiration): When this token expires, 7 days from now. 
                - scope: What this particular JWT can be used for, in this case it is an email_token which means it can only be used to verify an email address.
        
        :param self: Represent the instance of the class
        :param data: dict: Pass in the data that will be encoded
        :return: A token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token       
    

    def get_email_from_token(self, token: str):
        
        """
        The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
        If the scope of the token is not 'email_token', then it raises an HTTPException. If there is a JWTError, it also raises 
        an HTTPException.
        
        :param self: Represent the instance of the class
        :param token: str: Pass the token to the function
        :return: The email that is stored in the payload of the token
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'email_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")   
    

auth_service = Auth()
