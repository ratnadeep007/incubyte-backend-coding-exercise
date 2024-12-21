from pydantic import BaseModel


class Doctor(BaseModel):
    id: int
    first_name: str
    last_name: str


class Location(BaseModel):
    id: int
    address: str


class DoctorLocation(BaseModel):
    """
    This indicates that a doctor works at a location. Locations can have
    multiple doctors, and doctors can have multiple locations
    """

    id: int
    doctor_id: int
    location_id: int


class DoctorSchedule(BaseModel):
    id: int
    doctor_id: int
    location_id: int
    start_time: str  # Example: "09:00", "10:00", "11:00", etc.
    end_time: str  # Example: "09:00", "10:00", "11:00", etc.


class DoctorAppointment(BaseModel):
    id: int
    doctor_id: int
    location_id: int
    patient_name: str
    time: str  # Example: "09:00", "10:00", "11:00", etc.
