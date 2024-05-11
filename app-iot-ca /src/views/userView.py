from fastapi import APIRouter, HTTPException
# from src.models.validation import Validation 
from src.models.baseModel import UserIn
from typing import List
from src.schemas.schema import (
    ListOutput, OutputObject
)
from ..services.userService import UserService

user_router = APIRouter(prefix='/user')

@user_router.get('/list_users', response_model=List[ListOutput], status_code=200)
async def list_users():
    try:
        users = await UserService.list_users()
        return ListOutput(users)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@user_router.get('/{id}}', response_model=OutputObject, status_code=200)
async def user_id(user_id: str):
    try:
        user = await UserService.user_id(user_id)
        return OutputObject(user)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@user_router.post('/create', response_model=None, status_code=201)
async def create_user(userIn: UserIn):
    try:
        await UserService.create_user(userIn)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@user_router.post('/update/{id}', response_model=None, status_code=201)
async def update_user(user_id: str, user_input: UserIn):
    try:
       await UserService.update_user(user_id, user_input)
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@user_router.delete('/delete/{user_id}', response_model=None, status_code=200)
async def user_delete(user_id: str):
    try:
        await UserService.delete_user(user_id) 
    except Exception as error:
        raise HTTPException(400, detail=str(error))

