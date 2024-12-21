from pydantic import BaseModel


class CreateDoctorAppointmentRequest(BaseModel):
    location_id: int
    patient_name: str
    time: str
