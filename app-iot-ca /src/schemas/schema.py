from pydantic import BaseModel
from typing import List
from bson import json_util
from datetime import datetime
import pandas as pd 
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

def ModelOutput(data):
    doc = ListOutput(data)
    
    dataOcc = []
    for item in doc:
        id = str(item["_id"])
        _id = id.split("'")[3]
        tt = str(item['time'])
        time = tt.split(':')
        tm = f'{time[0]}:{time[1]}'

        oc ={
            "_id": _id,
            "identifier": item['identifier'],
            "heartbeat": item['heartbeat'],
            "X": item['X'],
            "Y": item['Y'],
            "Z": item['Z'],
            "time": tt,
        }
        dataOcc.append(oc)
    
    return dataOcc

def ListAnalyseOccurrenceOutput(data) -> list:
    doc = ListOutput(data)  
    dataOcc = []
    for occ in doc:
        oc ={
            "identifier": occ['identifier'],
            "occurrence": occ['body']['occurrence'],
            "location": occ['body']['location'],
            "occurrence_date": occ['body']['occurrence_date']
        }
        dataOcc.append(oc)
    
    return dataOcc

def ListAnalyseDataOutput(data) -> list:
    doc = ListOutput(data)
    new_datas = []
    
    for item in doc:
        id = str(item["_id"])
        _id = id.split("'")[3]
        dtt = item['datecreate']["$date"]
        #datecreate = datetime.strptime(dtt, "%m/%d/%Y %H:%M:%S")
        #datecreate = pd.to_datetime(dtt, "%m/%d/%Y %H:%M:%S.%f")
        
        for body in item['body']:
            datecollect = body['datecollect'].split('T')
            date = datecollect[0]
            time = datecollect[1].split('.')[0]
            days = date.split('-')
             
            df = {
                "_id": _id,
                "identifier": item['identifier'],
                "heartbeat": body['heartbeat'],
                "X": body['moviments']['X'],
                "Y": body['moviments']['Y'],
                "Z": body['moviments']['Z'],
                "date": date,
                "time": time,
                "days": days[2],
                #"datecreate": datecreate,
            }
            new_datas.append(df)
        
    return new_datas

def ListOutputPatient(patient, contacts, datas) -> list:
   return {
       "patient": OutputObject(patient),
       "contacts": OutputObject(contacts),
       "datas": List[ListOutput(datas)]
   }


# def TT(doc):
#     new_datas = []
#     for item in doc:
#         response = str(item["_id"])
#         _id = response.split("'")[3]

#         datacreate = str(item['datacreate']["$date"])

#         for body in item['body']:
            
#             X = str(body['moviments']['X']).split("'")[1]
#             Y = str(body['moviments']['Y']).split("'")[1]
#             Z = str(body['moviments']['Z']).split("'")[1]
#             heartbeat = str(body['heartbeat']).split("'")[1]

#             datecollect = str(body['datecollect']).split("'")[1].split("T")
          
#             hourCollect = datecollect[1].split(":")[0]

#             date = datecollect[1].split("-")
#             dayCollect = date[2]
#             mothCollect = date[1]
#             yearCollect = date[0]

#             df = {
#                 "_id": _id,
#                 "identifier": item['identifier'],
#                 "heartbeat": int(heartbeat),
#                 "X": int(X),
#                 "Y": int(Y),
#                 "Z": int(Z),
#                 #"datecollect": body['datecollect'],
#                 "dayCollect": int(dayCollect),
#                 "mothCollect": int(mothCollect),
#                 "yearCollect": int(yearCollect),
#                 "hourCollect": int(hourCollect),
#                 "datacreate": datacreate,
#             }
#             new_datas.append(df)
