from fastapi import HTTPException
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from ..database.connection import ApiSecurity, UserAuth, UserRobo, Certificate
from src.models.baseModel import SecurityIn
from ..schemas.schema import OutputObject
from pydantic import ValidationError
from datetime import datetime
from typing import List
import secrets
import random
import rsa

secretKey = str(secrets.token_hex(2024))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

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
                "date_create": datetime.now()
            }
            endPoints.append(body)

        ApiSecurity.insert_many(endPoints)
        #print(endPoints)
    async def create_secret_key(): 
        private_key = secrets.token_hex(156)
        public_key = secrets.token_hex(156)
        robo_key  = secrets.token_hex(128)

        body ={
            "private_key":  private_key,
            "public_key":  public_key,
            "robo_key":  robo_key
        }
        Certificate.insert_one(body)

    async def get_private_key(): 
        key = OutputObject(Certificate.find())
        #private_key = key["body"]["private_key"]
        return key

    def get_public_key() -> str: 
        key = OutputObject(Certificate.find())
        return key["body"]["public_key"]

    def decrypt_data(data) -> dict:
        key = OutputObject(Certificate.find())
        privite_key = key["body"]["public_key"]
        doc = rsa.decrypt(data, privite_key).decode() 
        return doc

    async def encrypt_data(data) -> dict:
        key = OutputObject(Certificate.find())
        privite_key = key["body"]["public_key"]
        doc = rsa.encrypt(data.encode(), privite_key) 
        return doc

    async def create_robo_user(identifier) -> dict:
        robo = random.randint(1000, 9999)
        password = random.randint(1000, 999999)
        certify_authorization = secrets.token_hex(8).encode()

        # key = OutputObject(Certificate.find())
        # private_key = key["body"]["public_key"]
        private_key = "6da82f8889859fca1394333bee5245b223e67f4954f490663bd645768ae730142dcd3be4e17875a028a30ad02e46bc70d7e9fe8a3c603321df6971831f004a9a8f47e6ead707d6bb41a68e75fb4fe44d6ff7592142b78d0bfe90e2ee98f8d26a59791a5cc262a21a98c5bc419cf9fd33125daa2932718f0565acdc678d083c997f3de42e93a5e613df469db075f09b0105dcb876d9f96cf2d5286ae3",

        body = {
            "identifier": identifier,
            "robo": robo,
            "password": rsa.encrypt(password.encode(), private_key),
            "certify_authorization ": certify_authorization,
            "create_date": datetime.now()
        }
        UserRobo.insert_one(body)
        print(body)

        resposne = {
            "identifier": identifier,
            "robo": robo,
            "password": password,
            "certify_authorization ": certify_authorization,
        }
        return resposne

    





    
    


