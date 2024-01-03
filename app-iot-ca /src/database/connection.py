import pymongo  
# from ..api.env import (DATABASE_URL, DATABASE_URL_ATLAS,
#                        DB_NAME)

DB_NAME='backoffice-iot'
DATABASE_URL=''
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
Datas = collection.Datas
Contacts = collection.Contacts
Doctor = collection.Doctor
ApiSecurity = collection.ApiSecurity
HistoryOccurrence = collection.HistoryOccurrence



