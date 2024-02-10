data_router = APIRouter(prefix='/data')

@data_router.post('/create/{identifier}', response_model=None, status_code=201)
async def create_data(identifier: int, dataIn: DataIn):
    try:
        if Validation.validator_datas(dataIn):
            patient = await PatientService.patient_identifier(identifier)
            patient_id = GetObjectId(patient)
            await DataService.create_datas(dataIn, identifier, patient_id)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    

#Nota: Os códigos completos estão em: app-iot-ca/views/dataView.py