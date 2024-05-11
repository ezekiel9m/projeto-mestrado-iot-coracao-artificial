from email_validator import validate_email, EmailNotValidError

null = None
class Validation:
    async def validator_user(item):
        body = item.body
        if body.name == null:
           raise ValueError("name connot be null")

    async def validator_datas(doc):
        body = doc.body

        if body.count() == 0:
            raise ValueError(" object request cannot be null")
        else:
            if body.moviments.X == null:
                raise ValueError("fild X is requied")
            if body.moviments.Y == null:
                raise ValueError("fild Y is requied")
            if body.moviments.Z == null:
                raise ValueError("fild Z is requied")
            if body.heartbeat == null:
                raise ValueError("fild heartbeat is requied")
            if body.datecollect == null:
                raise ValueError("fild datecollect is requied")
                
    
    async def validator_contacts(doc):
        body = doc.body

        if len(body) == 0:
            raise ValueError(" contact cannot be null")
        else:
            if body.phone_number == null:
                raise ValueError("fild phone number is requied")
            if body.contact_name == null:
                raise ValueError("fild contact name is requied")
            if body.degree_kinship == null:
                raise ValueError("fild degree kinship is requied")
            if body.contact_email == null:
                raise ValueError("fild contact email is requied")
            else:
                _validate_email(body.contact_email)

    async def validator_patient(doc):
        body = doc.body

        if doc == null:
            raise ValueError(" object request cannot be null")
        else:
            if doc.identifier == null:
                raise ValueError("fild identifier is requied")
            if doc.doctor_id == null:
                raise ValueError("fild doctor id is requied")
            if body.firstname == null:
                raise ValueError("fild first name is requied")
            if body.lastname == null:
                raise ValueError("fild last name is requied")
            if body.phonenumber == null:
                raise ValueError("fild phone number is requied")
            if body.email == null:
                raise ValueError("fild email is requied")
            else:
                _validate_email(body.email)
               
def _validate_email(email):
    try:
         validate_email(email)
    except EmailNotValidError as error:
        raise EmailNotValidError()

