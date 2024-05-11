from src.services.securityService import SecurityService
from ..models.baseModel import UserIn
from ..database.connection import User
from datetime import datetime
from bson import ObjectId
import rsa 

class UserService:
    async def list_users() -> list:
        users = User.find()
        return users

    async def user_id(user_id: str) -> dict:
        user = User.find_one({"_id": ObjectId(user_id)})
        return dict(user)

    async def create_user(userIn: UserIn):

        privite_key = SecurityService.get_private_key()
        user = {
            "body":{
                "firstname": userIn.body.firstname,
                "lastname": userIn.body.lastname,
                "email": userIn.body.email,
                "username": userIn.body.username,
                "password": rsa.encrypt(userIn.body.password.encode(), privite_key),
                "isActive": True,
                "datecreate": datetime.now()
            }
        }
        User.insert_one(user)
    
    async def update_user(user_id: str, userIn: UserIn):
        await User.update_one(
            { "_id": user_id },
            {
                "set": 
                { 
                    "name": userIn.name,
                    "lastname": userIn.lastname,
                    "email": userIn.email,
                    "phone": userIn.phone,
                    "date_create": datetime.new
                },
                "date_update": datetime.new
            }
        )

    async def delete_user(user_id: str):
        await User.delete_one({"_id": user_id})


