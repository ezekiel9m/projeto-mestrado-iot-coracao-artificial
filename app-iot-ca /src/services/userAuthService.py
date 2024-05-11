import jwt 
import rsa 
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from src.services.securityService import SecurityService
from src.services.userService import User
from ..database.connection import ApiSecurity
from datetime import datetime
from src.schemas.schema import OutputObject
from pydantic import ValidationError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

class UserAuthService:
    def auth_token(self, user_id, identifier):
        try:
            private_key = SecurityService.get_private_key()

            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id,
                'ident': identifier
            }
            return jwt.encode(
                payload,
                private_key,
                algorithm='HS256'
            )
        except Exception as e:
            return e
        
       
    def verify_robo_user(robo, password):
        try:
            private_key = SecurityService.get_private_key()

            roboUser = ApiSecurity.find_one({"robo": robo})
            usr = OutputObject(roboUser)
            user= usr["body"]["robo"]

            _password = rsa.encrypt(password.encode(), private_key),
            hashed_password= usr["body"]["password"]

            if user != robo : raise credentials_exception
            if not pwd_context.verify(_password, hashed_password): raise credentials_exception

        except JWTError:
            raise credentials_exception
        
    def verify_user(username, password):
        try:
            private_key = SecurityService.get_private_key()

            doc = User.find_one({"user_name": username})
            usr = OutputObject(doc)
            user = usr["body"]["user_name"]
            isActive = usr["body"]["isActive"]

            if isActive == False : raise ValidationError("user is no active")
            else:
                _password = rsa.encrypt(password.encode(), private_key),
                hashed_password= usr["body"]["password"]

                if user != username : raise credentials_exception
                if not pwd_context.verify(_password, hashed_password): raise credentials_exception

        except JWTError:
            raise credentials_exception