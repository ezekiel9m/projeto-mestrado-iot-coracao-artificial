from pydantic import BaseModel

class DefaultModel(BaseModel):
  firstname: str
  lastname: str
  age: int
  weight: int
  sex: str
  phonenumber: str
  email: str

class BoardModel(BaseModel):
  boad: str
  model: str
  version: str
  manufacturing_year: int

class contactsModel(BaseModel): 
  phonenumber: str
  contactname: str
  contactemail: str
  degreekinship: str

class BaseDataInModel(BaseModel):
  identifier: int 
  heartbeat: int 
  X: int 
  Y: int 
  Z: int 
  time: str
  
class Moviments(BaseModel):
  X: int 
  Y: int 
  Z: int 
  
class DataModel(BaseModel):
  moviments: Moviments
  heartbeat: int 
  location: str
  datecollect: str
  timecollect: str

class UserModel(BaseModel):
  firstname: str 
  lastname: str
  username: str
  password: str 
  confirmpassword: str
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
  occurrencedate: str