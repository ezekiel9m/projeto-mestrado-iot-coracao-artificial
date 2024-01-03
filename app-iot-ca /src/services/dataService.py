from src.models.baseModel import DatasIn
from ..database.connection import Datas, Patient, HistoryOccurrence
from datetime import datetime
from typing import List
from bson import ObjectId

class DataService:

    async def list_datas():
        datas = Datas.find()
        return list(datas)
    
    async def list_patient_datas(identifier: str):
        response = Patient.find({"identifier": identifier})
        return response

    async def datas_id(data_id: str):
        return Datas.find_one({"_id": ObjectId(data_id)})

    async def create_datas(datasIn: DatasIn, identifier: str, patient_id: str):
        bodys = []
        
        for item in datasIn.body: 
            body = {
                "moviments": {
                        "X": item.moviments.X,
                        "Y": item.moviments.Y,
                        "Z": item.moviments.Z,
                    },
                "heartbeat": item.heartbeat,
                "location": item.location,
                "datecollect": item.datecollect,
            }
            bodys.append(body)

        data ={
            "patient_id": patient_id,
            "identifier": identifier,
            "body": bodys,
            "datacreate": datetime.now()
        }
        Datas.insert_one(data)
    
    async def delete_patient(data_id: str):
        await Datas.delete_one({"_id": data_id})

    async def create_history_occurrence(identifier, data):
        occurrence ={
            "identifier": identifier,
            "body": {
                "occurrence": data.occurrence,
                "location": data.location,
                "occurrence_date": data.occurrence_date
            },
            "datacreate": datetime.now()
        }
        HistoryOccurrence.insert_one(occurrence)
    
    async def get_history_occurrence(identifier) -> list:
       return  HistoryOccurrence.find({"identifier": identifier})





