from typing import List
from fastapi import Depends, HTTPException, status, Request
from src.db.models import User, Role
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: List[Role]):
        
        """
        The __init__ function is called when the class is instantiated.
            It sets up the instance of the class with a list of allowed roles.
        
        :param self: Represent the instance of the class
        :param allowed_roles: List[Role]: Define the allowed roles for this command
        :return: Nothing
        :doc-author: Trelent
        """
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, current_user: User = Depends(auth_service.get_current_user)):
        
        """
        The __call__ function is the actual decorator.
        It takes a function as an argument and returns another function.
        The returned function will be called by FastAPI to handle requests.
        
        :param self: Represent the instance of the class
        :param request: Request: Get the request object
        :param current_user: User: Get the current user from the auth_service
        :return: A decorated function
        :doc-author: Trelent
        """
        print(request.method, request.url)
        print(f'User role {current_user.role}') #24/02/2024 Olha
        print(f'Allowed roles: {self.allowed_roles}') #Дозволені ролі
        if current_user.role not in self.allowed_roles: #24/02/2024 Olha
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Operation forbidden')