from fastapi import APIRouter, HTTPException
# from src.models.validation import Validation 
from src.models.baseModel import PatientIn
from typing import List
from src.schemas.schema import (
    ListOutput, OutputObject, ListOutputPatient, GetObjectId
)
from ..services.patientService import PatientService
from ..services.contactService import ContactService
from ..services.dataService import DataService

patient_router = APIRouter(prefix='/patient')

@patient_router.get('/list_patients', status_code=200)
async def list_patients():
    try:
        patients = await PatientService.list_patients()
        return  ListOutput(patients)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@patient_router.get('/{_id}', status_code=200)
async def get_patient_id(_id: str):
    try:
        patient = await PatientService.patient_id(_id)
        response = OutputObject(patient)
        identifier = response["identifier"]

        contact = await ContactService.list_patient_contacts(identifier)
        dadas = await DataService.list_patient_data(identifier)
        return ListOutputPatient(patient, contact, dadas)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@patient_router.get('/get/{identifier}', status_code=200)
async def get_patient_identifier(identifier: int):
    try:
        patient = await PatientService.patient_identifier(identifier)
        contact = await ContactService.list_patient_contacts(identifier)
        dadas = await DataService.list_patient_data(identifier)
        return ListOutputPatient(patient, contact, dadas)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@patient_router.post('/create', status_code=201)
async def create_patient(patientIn: PatientIn):
    try:
       response = await PatientService.create_patient(patientIn)
       return response
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@patient_router.post('/update/{id}', status_code=201)
async def update_patient(patient_id: str, patientIn: PatientIn):
    try:
       await PatientService.update_patient(patient_id, patientIn)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@patient_router.delete('/delete/{patient_id}', status_code=200)
async def user_delete(patient_id: str):
    try:
        await PatientService.delete_patient(patient_id) 
    except Exception as error:
        raise HTTPException(400, detail=str(error))

