from ..schemas.schema import  OutputObject, ListOutputPatient
from ..database.connection import Datas, Patient, Contacts
from ..steps.sendNotificationStep import send_whatsapp, send_email, report_data_analizy


class NotificationService:
    async def send_notification(identifier: str, data):
        await send_whatsapp(identifier, data)
        await send_email(identifier, data)

    async def send_whatsapp(identifier: str, data):
        contact = Contacts.find_one({'type': 'standar'})
        result = OutputObject(contact)
        phoneOrigen = result['standarPhone']

        listContacts = Contacts.find_one({'identifier': identifier})
        patient = Patient.find_one({'identifier': identifier})
        
        phones = []
        response = ListOutputPatient(patient, listContacts, None)

        for item in response['contacts']['body']: 
            phones.append({
                "name_destiny": item['contactName'], 
                "phone_destiny": item['phoneNumber']   
            })
        
        firstname  = response['patient']['body']['firstName']
        lastname  = response['patient']['body']['lastName']
        name = f'{firstname} {lastname}'
        await send_whatsapp(data, phones, name, phoneOrigen)

    async def send_email(identifier, data):
        patient = Patient.find_one({'identifier': identifier})
        
        response = OutputObject(patient)
        email = response['body']['email']
        name  = response['body']['firstName']
        
        file = report_data_analizy(identifier)
        await send_email(email, name, file)

