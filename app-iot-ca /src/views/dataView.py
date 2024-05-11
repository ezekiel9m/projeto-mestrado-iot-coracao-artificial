from fastapi import APIRouter, HTTPException, Header
from typing import Annotated
from src.models.validation import Validation 
from src.models.baseModel import DataIn, BaseDataModelIn
from typing import List
from src.schemas.schema import (
    ListOutput, OutputObject, GetObjectId
)
from src.services.dataService import DataService
from src.services.patientService import PatientService
from src.services.securityService import SecurityService

data_router = APIRouter(prefix='/data')

@data_router.get('/list_all', status_code=200)
async def list_data(api_key: Annotated[str | None, Header(convert_underscores=False)] = None):
    try: 
        #return await SecurityService.check_api_key(api_key)
        if await SecurityService.check_api_key(api_key):
            response = await DataService.list_data()
            return ListOutput(response)
        
    except Exception as error:
        raise HTTPException(400, detail=str(error))

# @data_router.get('/list_data_analyse', status_code=200)
# async def list_data_analyse():
#     try:
#         response = await DataService.list_datas()
#         result = await DataService.list_history_occurrence()
#         return ListAnalyseDateOutput(response, result)
#     except Exception as error:
#         raise HTTPException(400, detail=str(error))

@data_router.get('/patient/{identifier}', status_code=200)
async def list_patient_data(identifier: int):
    try:
        response = await DataService.list_patient_datas(identifier)
        return ListOutput(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@data_router.get('/{data_id}', status_code=200)
async def data_id(data_id: str):
    try:
        response = await DataService.data_id(data_id)
        return OutputObject(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@data_router.post('/create/{identifier}', response_model=None, status_code=201)
async def create_data(identifier: int, dataIn: DataIn):
    try:
        if Validation.validator_datas(dataIn):
            patient = await PatientService.patient_identifier(identifier)
            patient_id = GetObjectId(patient)
            await DataService.create_data(dataIn, identifier, patient_id)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@data_router.post('/data_model', response_model=None, status_code=201)
async def create_data_model(dataModelIn: BaseDataModelIn):
    try:
         await DataService.create_data_model(dataModelIn)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@data_router.get('/history_occurrence/{identifier}', status_code=200)
async def get_history_occurrence (identifier: int):
    try:
       historyOccurrence = await DataService.get_history_occurrence(identifier)
       return ListOutput(historyOccurrence)
    except Exception as error:
        raise HTTPException(400, detail=str(error))







