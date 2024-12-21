from .doctor import Doctor, Location, DoctorLocation
from .requests.add_doctor_request import AddDoctorRequest
from .requests.create_doctor_schedule_request import CreateDoctorScheduleRequest
from .requests.create_doctor_appointment_request import CreateDoctorAppointmentRequest

__all__ = [
    "Doctor",
    "Location",
    "DoctorLocation",
    "AddDoctorRequest",
    "CreateDoctorScheduleRequest",
    "CreateDoctorAppointmentRequest",
]
