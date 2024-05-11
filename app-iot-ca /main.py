from fastapi import FastAPI, APIRouter
from src.views.userView import user_router
from src.views.patientView import patient_router
from src.views.contactView import contact_router
from src.views.dataView import data_router
from src.views.doctorView import doctor_router
from src.views.securityView import security_router
from src.views.analyseView import analyse_router
from src.views.notificationView import notification_router
from src.views.userAuthView import user_auth_router

app = FastAPI(title="Projeto Coaração Artificial")
router = APIRouter()
app = FastAPI()

app.include_router(user_router)
app.include_router(data_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(contact_router)
app.include_router(security_router)
app.include_router(analyse_router)
app.include_router(user_auth_router)
app.include_router(notification_router)

import os
import ssl                                        
openssl_dir, openssl_cafile = os.path.split(      
    ssl.get_default_verify_paths().openssl_cafile)
# no content in this folder
os.listdir(openssl_dir)