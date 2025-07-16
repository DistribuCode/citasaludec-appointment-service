from fastapi import APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.controllers import appointmentController
from src.middlewares.authMiddleware import verify_jwt
from src.models.appointmentModel import Appointment

security = HTTPBearer()
router = APIRouter()

@router.get("/", tags=["Appointments"])
async def get_appointments(credentials: HTTPAuthorizationCredentials = Security(security)):
    verify_jwt(credentials)
    return await appointmentController.get_appointments()

@router.post("/", tags=["Appointments"])
async def create_appointment(
    appointment: Appointment,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    verify_jwt(credentials)
    token = credentials.credentials  # ✅ Extrae el JWT correctamente
    return await appointmentController.create_appointment(appointment.dict(), token)
