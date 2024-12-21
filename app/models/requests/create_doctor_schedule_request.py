from pydantic import BaseModel


class CreateDoctorScheduleRequest(BaseModel):
    location_id: int
    start_time: str
    end_time: str
