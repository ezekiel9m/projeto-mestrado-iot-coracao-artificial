from src.models.baseModel import DataIn, DataOccurrenceIn, BaseDataModelIn
from ..database.connection import Data, Patient, HistoryOccurrence, DataModel
from src.services.securityService import SecurityService
from datetime import datetime
from typing import List
from bson import ObjectId

class DataService:

    async def list_data():
        data = Data.find()
        return list(data)
    
    async def list_patient_data(identifier: int):
        response = Patient.find({"identifier": identifier})
        return response

    async def Data_id(data_id: str):
        return Data.find_one({"_id": ObjectId(data_id)})

    async def create_data(DataIn: DataIn, identifier: str, patient_id: str, patient_number: int):
        bodys = []

        for item in DataIn.body: 
            body = {
                "moviments": {
                        "X": item.moviments.X,
                        "Y": item.moviments.Y,
                        "Z": item.moviments.Z,
                    },
                "heartbeat": item.heartbeat,
                "location": item.location,
                "datecollect": item.datecollect,
                "datecollect": item.timecollect,
            }
            encodeBody = SecurityService.encrypt_data(body)
            bodys.append(encodeBody)

        data ={
            "patient_id": patient_id,
            "patient_number": patient_number,
            "identifier": identifier,
            "body": bodys,
            "datecreate": datetime.now()
        }
        Data.insert_one(data)
    
    async def create_data_model(dataModelIn: BaseDataModelIn):
        data = []
        for item in dataModelIn.data: 
            body = {
                "heartbeat": item.heartbeat,
                "X": item.X,
                "Y": item.Y,
                "Z": item.Z,
                "time": item.time,
            }
            data.append(body)

        DataModel.insert_many(data)
    
    
    async def delete_patient(data_id: str):
        await Data.delete_one({"_id": data_id})

    async def create_history_occurrence(identifier: int, data: DataOccurrenceIn):
        return identifier
        body ={
                "occurrence": data.occurrence,
                "location": data.location,
                "type": data.type,
                "occurrence_date": data.occurrence_date
        }
        encodeBody = encrypt_data(body)
        occurrence ={
            "identifier": identifier,
            "body": encodeBody,
            "datecreate": datetime.now()
        }
        HistoryOccurrence.insert_one(occurrence)
    
    async def get_history_occurrence(identifier) -> list:
       return  HistoryOccurrence.find({"identifier": identifier})
    





