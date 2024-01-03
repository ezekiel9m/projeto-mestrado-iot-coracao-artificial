from ..models.baseModel import UserIn
from ..database.connection import User
from datetime import datetime
from bson import ObjectId

class UserService:
    async def list_users() -> list:
        users = User.find()
        return list(users)

    async def user_id(user_id: str) -> dict:
        user = User.find_one({"_id": ObjectId(user_id)})
        return dict(user)

    async def create_user(userIn: UserIn):
        user = {
            "body":{
                "first_name": userIn.body.first_name,
                "last_name": userIn.body.last_name,
                "email": userIn.body.email,
                "user_name": userIn.body.user_name,
                "password": userIn.body.password,
                "isActive": True,
                "data_create": datetime.now()
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
                    "datacreate": datetime.new
                },
                "dataupdate": datetime.new
            }
        )

    async def delete_user(user_id: str):
        await User.delete_one({"_id": user_id})


