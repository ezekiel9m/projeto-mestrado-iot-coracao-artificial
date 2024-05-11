from pydantic import BaseModel
from typing import List
from ..models.models import (DefaultModel, PasswordModel,WhatsappModel,
                             UserModel, DataModel, contactsModel, SecurityModel,
                             DataOccurrenceModel, BaseDataInModel, BoardModel
                            )

class PatientIn(BaseModel): 
  doctor_id: str
  number: int
  body: DefaultModel
  board: BoardModel

class DoctorIn(BaseModel): body: DefaultModel
class UserIn(BaseModel): body: UserModel
class PasswordIn(BaseModel): PasswordModel

class DataIn(BaseModel): body: List[DataModel]
class BaseDataModelIn(BaseModel): data : List[BaseDataInModel]

class ContactIn(BaseModel): 
  patient_id: str
  identifier: int
  body: List[contactsModel]
class WhatssapIn(BaseModel): WhatsappModel

class SecurityIn(BaseModel): body: List[SecurityModel]
class DataOccurrenceIn(BaseModel): 
  occurrence: str
  location: str
  occurrence_date: str
  type: str

class Login(BaseDataInModel):
  username: str
  password: str

class LoginRobo(BaseDataInModel):
  robo: str
  password: str


  



