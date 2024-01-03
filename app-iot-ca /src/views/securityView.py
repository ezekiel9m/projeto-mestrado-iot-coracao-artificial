from fastapi import APIRouter, HTTPException, Header
from typing import Annotated
from pydantic import ValidationError
from src.models.baseModel import SecurityIn
from ..schemas.schema import (
    ListOutput, OutputObject
)
from ..services.securityService import SecurityService

security_router = APIRouter(prefix='/security')

@security_router.get('/list_apiKey', status_code=200)
async def list_apiKey():
    try:
        response = await SecurityService.list_apiKey()
        return ListOutput(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@security_router.get('/{_id}', status_code=200)
async def get_api_key(_id: str):
    try:
        response = await SecurityService.get_api_key(_id)
        return OutputObject(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@security_router.get('/check_api_key/{api_key}')
async def check_api_key(api_key: str):
    try:
        return await SecurityService.check_api_key(api_key)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@security_router.post('/create', status_code=201,)
async def create_api_key(securityIn: SecurityIn,
                          api_key: Annotated[str, Header(convert_underscores=True)]):
    try:
        checkKey = await SecurityService.check_api_key(api_key)
        if  checkKey == True:
            if securityIn.body.count == 0:
                raise ValidationError("end_point is requied")
            else:
                await SecurityService.create_api_key(securityIn)
    except Exception as error:
        raise HTTPException(400, detail=str(error))



