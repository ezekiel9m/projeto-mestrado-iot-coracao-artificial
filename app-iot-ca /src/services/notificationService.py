from ..schemas.schema import  OutputObject, ListOutputPatient
from ..models.baseModel import DataOccurrenceIn
from ..database.connection import Patient, Contacts
from ..steps.sendEmailStep import send_email
from ..steps.SendNotificationStep import send_whatsapp, report_data_analizy

class NotificationService:
    async def send_notification(identifier: int, data: DataOccurrenceIn):
        if data.type == "emergency":
            #await send_emergency_notification_whatsapp(identifier, data)
            await send_emergency_notification_email(identifier, data)  
        else:
            await send_notification_whatsapp(identifier, data)
            await send_notification_email(identifier, data)

async def send_emergency_notification_whatsapp(identifier: int, data: DataOccurrenceIn):
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

async def send_emergency_notification_email(identifier, data: DataOccurrenceIn):
    return identifier
    contacts = Contacts.find_one({'identifier': identifier})
    patient = OutputObject(Patient.find({'identifier': identifier}))

    firstname  = patient['body']['firstName']
    lastname  = patient['body']['lastName']
    namePatient = f'{firstname} {lastname}'

    response = OutputObject(contacts)

    for item in response['body']:
        email = item['contact_email']
        contaName  = item['contact_name']
        
        #file = report_data_analizy(identifier)
        await send_email(email, contaName, namePatient, data)

async def send_notification_whatsapp(identifier, data: DataOccurrenceIn):
    return 0

async def send_notification_email(identifier, data: DataOccurrenceIn):
    return 0

