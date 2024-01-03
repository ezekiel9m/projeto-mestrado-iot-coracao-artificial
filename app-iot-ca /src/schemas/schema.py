from pydantic import BaseModel
from typing import List
from bson import json_util
from datetime import datetime
import json
import bson


def OutputObject(item) -> dict:
    doc = json_util.dumps(item)
    return json.loads(doc)

class StandardOutput(BaseModel):
    message: str

class ErrorOutput(BaseModel):
    detail: str

def GetObjectId(item):
    doc = json_util.dumps(item)
    result = json.loads(doc)
    response = str(result["_id"])
    _id = response.split("'")[3]
    return _id

def ListOutput(item) -> list:
    doc = json_util.dumps(item)
    return json.loads(doc)

def ListAnalyseDateOutput(item) -> list:
    doc = ListOutput(item)
    new_datas = []
    for item in doc:
        response = str(item["_id"])
        _id = response.split("'")[3]

        datacreate = str(item['datacreate']["$date"])

        for body in item['body']:
            
            X = str(body['moviments']['X']).split("'")[1]
            Y = str(body['moviments']['Y']).split("'")[1]
            Z = str(body['moviments']['Z']).split("'")[1]
            heartbeat = str(body['heartbeat']).split("'")[1]

            datecollect = str(body['datecollect']).split("'")[1].split("T")
          
            hourCollect = datecollect[1].split(":")[0]

            date = datecollect[1].split("-")
            dayCollect = date[2]
            mothCollect = date[1]
            yearCollect = date[0]

            df = {
                "_id": _id,
                "identifier": item['identifier'],
                "heartbeat": int(heartbeat),
                "X": int(X),
                "Y": int(Y),
                "Z": int(Z),
                #"datecollect": body['datecollect'],
                "dayCollect": int(dayCollect),
                "mothCollect": int(mothCollect),
                "yearCollect": int(yearCollect),
                "hourCollect": int(hourCollect),
                "datacreate": datacreate,
            }
            new_datas.append(df)
    return new_datas

def ListOutputPatient(patient, contacts, datas) -> list:
   return {
       "patient": OutputObject(patient),
       "contacts": OutputObject(contacts),
       "datas": List[ListOutput(datas)]
   }
