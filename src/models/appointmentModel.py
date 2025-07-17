from pydantic import BaseModel, Field
from datetime import date

class Appointment(BaseModel):
    patient: int = Field(..., gt=0, description="ID del paciente")
    patient_name: str = Field(..., min_length=2)
    disease: str = Field(..., min_length=3)
    date: date 
