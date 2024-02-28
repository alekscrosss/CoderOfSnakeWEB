from pathlib import Path
import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import auth_service
from dotenv import load_dotenv
load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM=os.environ.get('MAIL_FROM'),
    MAIL_PORT=os.environ.get('MAIL_PORT'),
    MAIL_SERVER=os.environ.get('MAIL_SERVER'),
    MAIL_FROM_NAME="Contacts app",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):
    
    """
    The send_email function sends an email to the user with a link to confirm their email address.
        Args:
            email (str): The user's email address.
            username (str): The username of the user who is registering for an account.
            host (str): The hostname of the server where this function is being run from.
    
    :param email: EmailStr: Define the recipient's email address
    :param username: str: Fill in the username field in the email template
    :param host: str: Pass the hostname of the server to the template
    :return: A coroutine object
    :doc-author: Trelent
    """
    try:
        # TODO def create_email_token
        token_verification = auth_service.create_email_token({"sub": email}) 
        message = MessageSchema(
            subject="Confirm your email", #це заголовок листа
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)
