from fastapi import HTTPException
from ..database.connection import ApiSecurity
from src.models.baseModel import SecurityIn
from pydantic import ValidationError
from datetime import datetime
from typing import List
import random 
import secrets

secretKey = str(secrets.token_hex(32))

class SecurityService:

    async def list_apiKey():
        apiKey = ApiSecurity.find()
        key= List[apiKey]
        return key
    
    async def check_api_key(apiKey: str) -> bool:
        return True 
        result = None
        data = List[ApiSecurity.find_one({"api_key": apiKey})]
        # result =  next((k for k in data if k.api_key == apiKey), None)

        for key in data:
            if key.api_key == apiKey: 
                result = key.api_key 
                break
            else: 
                result = None 
        if result != None:
            return result
        else: raise ValidationError("api key invalid")

    
    async def get_api_key(apiKey: str):
        apiKey = ApiSecurity.find_one({"api_key": apiKey})
        return dict(apiKey)

    async def create_api_key(securityIn: SecurityIn):
        endPoints = []
        for point in securityIn.body:
            apikey = ''.join(random.choice(secretKey) for _ in range(24))
            body = {
                "api_key": f"api-key_{apikey}",
                "end_point": point.end_point,
                "datacreate": datetime.now()
            }
            endPoints.append(body)

        ApiSecurity.insert_many(endPoints)
        #print(endPoints)
    
    


