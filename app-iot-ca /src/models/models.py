from pydantic import BaseModel

class DefaultModel(BaseModel):
  first_name: str
  last_name: str
  phone_number: str
  email: str

class contactsModel(BaseModel): 
  phone_number: str
  contact_name: str
  contact_email: str
  degree_kinship: str

class Moviments(BaseModel):
  X: str
  Y: str
  Z: str
  
class DataModel(BaseModel):
  moviments: Moviments
  heartbeat: str
  location: str
  datecollect: str

class UserModel(BaseModel):
  firstname: str 
  lastname: str
  username: str
  password: str = None
  confirmpassword: str = None
  email: str

class PasswordModel(BaseModel):
  newPassword: str
  confirmPassword: str

class WhatsappModel(BaseModel):
  name_destiny: str
  phone_destiny: str

class SecurityModel(BaseModel):
  end_point: str

class DataOccurrenceModel(BaseModel):
  occurrence: str
  location: str
  occurrence_date: str