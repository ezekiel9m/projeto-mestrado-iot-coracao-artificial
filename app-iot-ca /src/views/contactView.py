from fastapi import APIRouter, HTTPException
from src.models.validation import Validation 
from src.models.baseModel import ContactIn
from pydantic import ValidationError
from ..schemas.schema import (
    ListOutput, OutputObject
)
from ..services.contactService import ContactService

contact_router = APIRouter(prefix='/contact')

@contact_router.get('/list_contacts', status_code=200)
async def list_contacts():
    try:
        response = await ContactService.list_contacts()
        return ListOutput(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@contact_router.get('/{_id}', status_code=200)
async def contact_id(_id: str):
    try:
        response = await ContactService.contact_id(_id)
        return OutputObject(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@contact_router.get('/patient/{identifier}', status_code=200)
async def list_patient_contacts(identifier: str):
    try:
        response = await ContactService.list_patient_contacts(identifier)
        return OutputObject(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@contact_router.post('/create', status_code=201)
async def create_contact(contactIn: ContactIn):
    try:
        if contactIn.count() > 3:
            raise ValidationError("Is requied only 3 contacts")
        else:
         if Validation.validator_contacts(contactIn):
            await ContactService.create_contact(contactIn)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@contact_router.post('/update/{contact_id}', status_code=201)
async def update_contact(contact_id: str, contactIn: ContactIn):
    try:
       await ContactService.update_contact(contact_id, contactIn)
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@contact_router.delete('/delete/{contact_id}', status_code=200)
async def delete_contact(contact_id: str):
    try:
        await ContactService.delete_contact(contact_id) 
    except Exception as error:
        raise HTTPException(400, detail=str(error))


