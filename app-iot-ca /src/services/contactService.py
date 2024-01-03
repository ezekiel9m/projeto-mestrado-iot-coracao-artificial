from src.models.baseModel import ContactIn
from ..database.connection import Contacts
from datetime import datetime
from bson import objectid

class ContactService:

    async def list_contacts():
        contacts = Contacts.find()
        return list(contacts)
    
    async def list_patient_contacts(identifier: str):
        contact = Contacts.find_one({"identifier": identifier})
        return dict(contact)

    async def contact_id(contact_id: str):
        contact = Contacts.find_one({"_id": objectid(contact_id)})
        return dict(contact)

    async def create_contact(contactIn: ContactIn):
        bodys = []
        count = 1
        for item in contactIn.body: 
            body = {
                "phone_number": item.phone_number,
                "contact_name": item.contact_name,
                "contact_email": item.contact_email,
                "degree_kinship": item.degree_kinship,
                "posion_phone": count
            }
            count += 1
            bodys.append(body)

        contacts ={
            "patient_id": contactIn.patient_id,
            "identifier": contactIn.identifier,
            "body": bodys,
            "date_create": datetime.now(),
        }
        Contacts.insert_one(contacts)
    
    async def update_contact(contact_id: str, contactIn: ContactIn):
        await Contacts.update_one(
            { "_id": contact_id },
            {
                "set": 
                { 
                    "_id": contactIn,
                    "name": contactIn.name,
                    "lastname": contactIn.lastname,
                    "email": contactIn.email,
                    "phone": contactIn.phone,
                    "datacreate": datetime.new
                },
                "dataupdate": datetime.new()
            }
        )

    async def delete_contact(contact_id: str):
        await Contacts.delete_one({"_id": contact_id})


