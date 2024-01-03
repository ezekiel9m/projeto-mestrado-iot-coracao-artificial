from pydantic import BaseModel
from typing import List
from ..models.models import (DefaultModel, PasswordModel,WhatsappModel,
                             UserModel, DataModel, contactsModel, SecurityModel,
                             DataOccurrenceModel
                            )

class PatientIn(BaseModel): 
  identifier: str
  doctor_id: str
  body: DefaultModel

class DoctorIn(BaseModel): body: DefaultModel
class UserIn(BaseModel): body: UserModel
class PasswordIn(BaseModel): PasswordModel

class DatasIn(BaseModel): body: List[DataModel]

class ContactIn(BaseModel): 
  patient_id: str
  identifier: str
  body: List[contactsModel]
class WhatssapIn(BaseModel): WhatsappModel

class SecurityIn(BaseModel): body: List[SecurityModel]
class DataOccurrenceIn(BaseModel): DataOccurrenceModel
  



