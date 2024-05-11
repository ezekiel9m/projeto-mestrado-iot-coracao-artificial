from fastapi import APIRouter, HTTPException
# from src.models.validation import Validation 
from src.models.baseModel import LoginRobo,  Login
from typing import List
from src.schemas.schema import (
    ListOutput, OutputObject
)
from ..services.userService import UserService
from ..services.securityService import SecurityService
from ..services.userAuthService import UserAuthService

user_auth_router = APIRouter(prefix='/user_auth')


@user_auth_router.post('/login', response_model=None, status_code=201)
async def ligin():
    try:
        return 0
    except Exception as error:
        raise HTTPException(400, detail=str(error))

