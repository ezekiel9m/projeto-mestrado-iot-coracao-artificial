from fastapi import APIRouter, HTTPException
# from models.validation import Validation 
from typing import List
from ..models.baseModel import DataOccurrenceIn
from ..schemas.schema import (
    ListOutput, OutputObject
)
from src.services.patientService import PatientService
from src.services.dataService import DataService

notification_router = APIRouter(prefix='/notification')

@notification_router.post('/send_notification/{identifier}')
async def send_notification(dataOccurrenceIn: DataOccurrenceIn, identifier: str):
    try:
        await PatientService.send_notification(identifier)
        await DataService.create_history_occurrence(identifier, dataOccurrenceIn)
    except Exception as error:
        raise HTTPException(400, detail=str(error))



