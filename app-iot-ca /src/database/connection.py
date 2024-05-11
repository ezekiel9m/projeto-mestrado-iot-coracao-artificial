import pymongo  
# from ..api.env import (DATABASE_URL, DATABASE_URL_ATLAS,
#                        DB_NAME)

DB_NAME='backoffice-iot'
DATABASE_URL='mongodb://127.0.0.1:27017'
DATABASE_URL_ATLAS =''
PASSWORD_BD=''


USER = 'User'
PATIENT = 'Patient'
DATAS = 'Datas'
CONTACTS = 'Contacts'
DOCTOR = 'Doctor'

connection = pymongo.MongoClient(DATABASE_URL_ATLAS) 
collection = connection[DB_NAME]

User = collection.User
Patient = collection.Patient
Data = collection.Data
Contacts = collection.Contacts
Doctor = collection.Doctor
ApiSecurity = collection.ApiSecurity
HistoryOccurrence = collection.HistoryOccurrence
DataModel = collection.DataModel
UserAuth = collection.UserAuth
UserRobo = collection.UserRobo
Certificate = collection.Certificate

