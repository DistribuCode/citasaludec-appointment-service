from pydantic import BaseModel

class Appointment(BaseModel):
    patient: str
    patient_name: str
    disease: str
    date: str  
