from src.models.baseModel import PatientIn
from ..database.connection import Patient
from datetime import datetime
from bson import ObjectId


class PatientService:

    async def list_patients():
        patients = Patient.find()
        return list(patients)

    async def patient_id(patient_id: str):
        patient = Patient.find_one({"_id": ObjectId(patient_id)})
        return dict(patient)
    
    async def patient_identifier(identifier: str):
        return Patient.find_one({"identifier": identifier})

    async def create_patient(patientIn: PatientIn):
        body = patientIn.body
        patient = {
            "identifier": patientIn.identifier,
            "doctor_id":  patientIn.doctor_id,
            "body":{
                "first_name": body.first_name,
                "last_name": body.last_name,
                "phone_number": f"+55{body.phone_number}",
                "email": body.email,
            },
            "data_create": datetime.now()
        }
        Patient.insert_one(patient)
    
    async def update_patient(patient_id: str, PatientIn: PatientIn):
        await Patient.update_one(
            { "_id": ObjectId(patient_id) },
            {
                "set": 
                { 
                    "_id": patient_id,
                    "first_name": PatientIn.first_name,
                    "last_name": PatientIn.last_name,
                    "email": PatientIn.email,
                    "phone": PatientIn.phone,
                    "datacreate": datetime.new()
                },
                "dataupdate": datetime.new()
            }
        )

    async def delete_patient(patient_id: str):
        await Patient.delete_one({"_id": patient_id})


