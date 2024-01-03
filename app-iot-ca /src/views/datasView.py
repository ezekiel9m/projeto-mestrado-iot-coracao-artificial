from fastapi import APIRouter, HTTPException, Header
from typing import Annotated
from src.models.validation import Validation 
from src.models.baseModel import DatasIn
from typing import List
from src.schemas.schema import (
    ListOutput, OutputObject, GetObjectId, ListAnalyseDateOutput
)
from src.services.dataService import DataService
from src.services.patientService import PatientService
from src.services.securityService import SecurityService

datas_router = APIRouter(prefix='/datas')

@datas_router.get('/list_all', status_code=200)
async def list_datas(api_key: Annotated[str | None, Header(convert_underscores=False)] = None):
    try: 
        #return await SecurityService.check_api_key(api_key)
        if await SecurityService.check_api_key(api_key):
            response = await DataService.list_datas()
            return ListOutput(response)
        
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@datas_router.get('/list_datas_analyse', status_code=200)
async def list_datas_analyse():
    try:
        response = await DataService.list_datas()
        return ListAnalyseDateOutput(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@datas_router.get('/patient/{identifier}', status_code=200)
async def list_patient_datas(identifier: str):
    try:
        response = await DataService.list_patient_datas(identifier)
        return ListOutput(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@datas_router.get('/{data_id}', status_code=200)
async def data_id(data_id: str):
    try:
        response = await DataService.datas_id(data_id)
        return OutputObject(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@datas_router.post('/create/{identifier}', response_model=None, status_code=201)
async def create_datas(identifier: str, datasIn: DatasIn):
    try:
        if Validation.validator_datas(datasIn):
            patient = await PatientService.patient_identifier(identifier)
            patient_id = GetObjectId(patient)
            await DataService.create_datas(datasIn, identifier, patient_id)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@datas_router.get('/history_occurrence/{identifier}', status_code=200)
async def get_history_occurrence (identifier: str):
    try:
       historyOccurrence = await DataService.get_history_occurrence(identifier)
       return ListOutput(historyOccurrence)
    except Exception as error:
        raise HTTPException(400, detail=str(error))







