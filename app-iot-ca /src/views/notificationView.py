from fastapi import APIRouter, HTTPException
# from models.validation import Validation 
from typing import List
from ..models.baseModel import DataOccurrenceIn
from ..schemas.schema import (
    ListOutput, OutputObject
)
from src.services.notificationService import NotificationService
from src.services.dataService import DataService

notification_router = APIRouter(prefix='/notification')

@notification_router.post('/send_notification/{identifier}', status_code=200)
async def send_notification(identifier: int, dataOccurrenceIn: DataOccurrenceIn):
    try:
       return await NotificationService.send_notification(identifier, dataOccurrenceIn)
        #await DataService.create_history_occurrence(identifier, dataOccurrenceIn)
    except Exception as error:
        raise HTTPException(400, detail=str(error))



