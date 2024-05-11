from fastapi import APIRouter, HTTPException, Header
from typing import Annotated
from src.schemas.schema import (
    ListAnalyseOccurrenceOutput, ListAnalyseDataOutput, ModelOutput
)
from src.services.analyseService import AnalyseService
from src.services.securityService import SecurityService

analyse_router = APIRouter(prefix='/analyse')

@analyse_router.get('/data_analyse', status_code=200)
async def list_datas_analyse(api_key: Annotated[str | None, Header(convert_underscores=False)] = None):
    try: 
        if await SecurityService.check_api_key(api_key):
            response = await AnalyseService.list_data_analyse()
        return ListAnalyseDataOutput(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@analyse_router.get('/occurrence_analyse', status_code=200)
async def list_history_occurrence_analyse(api_key: Annotated[str | None, Header(convert_underscores=False)] = None):
    try:
        response = await AnalyseService.list_history_occurrence_analyse()
        return ListAnalyseOccurrenceOutput(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@analyse_router.get('/data_model', status_code=200)
async def list_datas_model():
    try: 
        response = await AnalyseService.list_data_model()
        return ModelOutput(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

