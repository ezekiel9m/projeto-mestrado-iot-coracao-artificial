class NotificationService:
    async def send_whatsapp(identifier: str, data):
        contact = Contacts.find_one({'type': 'standar'})
        result = Output(contact)
        phoneOrigen = result['standarPhone']

        listContacts = Contacts.find_one({'identifier': identifier})
        patient = Patient.find_one({'identifier': identifier})
        
        phones = []
        response = PatientOutput(patient, listContacts, None)

        for item in response['contacts']['body']: 
            phones.append({
                "name_destiny": item['contactName'], 
                "phone_destiny": item['phoneNumber']   
            })
        
        firstname  = response['patient']['body']['firstName']
        lastname  = response['patient']['body']['lastName']
        name = f'{firstname} {lastname}'
        await send_messager_whatsapp(data, phones, name, phoneOrigen)

    async def send_email(identifier):
        patient = Patient.find_one({'identifier': identifier})
        
        response = Output(patient)
        email = response['body']['email']
        name  = response['body']['firstName']
        
        file = report_data_analizy(identifier)
        send_email(email, name, file)


#Nota: Os códigos completos estão em: app-iot-ca/services/notificationService