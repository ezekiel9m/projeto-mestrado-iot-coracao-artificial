from src.models.baseModel import PatientIn
from ..database.connection import Patient
from src.services.securityService import SecurityService
from datetime import datetime
from bson import ObjectId
import random 

class PatientService:
    async def list_patients():
        patients = Patient.find()
        return patients

    async def patient_id(patient_id: str):
        patient = Patient.find_one({"_id": ObjectId(patient_id)})
        return dict(patient)
    
    async def patient_identifier(identifier: int):
        return Patient.find_one({"identifier": identifier})

    async def create_patient(patientIn: PatientIn) -> dict:
        identifier = random.randint(1000, 9999999)

        body = patientIn.body
        board = patientIn.board
        patient = {
            "identifier": identifier,
            "number":patientIn.number,
            "doctor_id":  patientIn.doctor_id,
            "body":{
                "firstname": body.firstname,
                "lastname": body.lastname,
                "age":body.age,
                "weight":body.weight,
                "sex":body.sex,
                "phonenumber": f"+55{body.phonenumber}",
                "email": body.email,
            },
            "board": {
                "boad":board.boad,
                "model": board.model,
                "version": board.version,
                "manufacturing_year": board.manufacturing_year
            },
            "datecreate": datetime.now()
        }
        Patient.insert_one(patient)
        response = await SecurityService.create_robo_user(identifier)
        return response
    
    async def update_patient(patient_id: str, PatientIn: PatientIn):
        await Patient.update_one(
            { "_id": ObjectId(patient_id) },
            {
                "set": 
                { 
                    "_id": patient_id,
                    "firstname": PatientIn.first_name,
                    "last_name": PatientIn.last_name,
                    "email": PatientIn.email,
                    "phone": PatientIn.phone,
                    "datecreate": datetime.new()
                },
                "dateupdate": datetime.new()
            }
        )

    async def delete_patient(patient_id: str):
        await Patient.delete_one({"_id": patient_id})

        


