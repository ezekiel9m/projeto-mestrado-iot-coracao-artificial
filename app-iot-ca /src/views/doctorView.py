from fastapi import APIRouter
# from models.validation import Validation 
from src.models.baseModel import PatientIn
from typing import List
from ..schemas.schema import (
    ListOutput, OutputObject
)
from src.services.patientService import PatientService

doctor_router = APIRouter(prefix='/doctor')