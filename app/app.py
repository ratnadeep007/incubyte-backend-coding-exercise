from typing import Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from app.database.db import DB
from app.models.error import NotFoundException, ResoruceAlreadyExistsException
from app.models import (
    AddDoctorRequest,
    CreateDoctorScheduleRequest,
    CreateDoctorAppointmentRequest,
)
from app.services.availability_service import AvailabilityService
from app.services.doctor_service import (
    DoctorService,
    InDatabaseDoctorService,
    InMemoryDoctorService,
)
from app.settings import Settings


def create_app() -> FastAPI:
    doctor_service: DoctorService
    availability_service: AvailabilityService
    db: Optional[DB] = None
    if Settings.in_database:
        db = DB()
        db.init_if_needed()
        doctor_service = InDatabaseDoctorService(db=db)
        availability_service = AvailabilityService(db=db)
    else:
        doctor_service = InMemoryDoctorService()
        doctor_service.seed()

    app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})

    @app.get("/doctors")
    def list_doctors():
        return doctor_service.list_doctors()

    @app.get("/doctors/{id}")
    async def get_doctor(id: int):
        return doctor_service.get_doctor(id)

    @app.post("/doctors")
    def add_doctor(request: AddDoctorRequest):
        id = doctor_service.add_doctor(
            first_name=request.first_name, last_name=request.last_name
        )

        return {"id": id}

    @app.get("/doctors/{doctor_id}/locations")
    def get_doctor_locations(doctor_id: int):
        return doctor_service.list_doctor_locations(doctor_id=doctor_id)

    # Add new endpoints here! #
    @app.get("/doctors/{doctor_id}/schedules")
    def get_doctor_schedules(doctor_id: int):
        return availability_service.list_doctor_schedules(doctor_id=doctor_id)

    @app.post("/doctors/{doctor_id}/schedules")
    def add_doctor_schedule(doctor_id: int, request: CreateDoctorScheduleRequest):
        id = availability_service.create_doctor_schedule(
            doctor_id=doctor_id,
            location_id=request.location_id,
            start_time=request.start_time,
            end_time=request.end_time,
        )
        return {"id": id}

    @app.get("/doctors/{doctor_id}/appointments")
    def get_doctor_appointments(doctor_id: int):
        return availability_service.list_doctor_appointments(doctor_id=doctor_id)

    @app.post("/doctors/{doctor_id}/appointments")
    def add_doctor_appointment(doctor_id: int, request: CreateDoctorAppointmentRequest):
        return availability_service.create_appointment(
            doctor_id=doctor_id,
            location_id=request.location_id,
            time=request.time,
            patient_name=request.patient_name,
        )

    @app.delete("/doctors/{doctor_id}/appointments/{appointment_id}")
    def delete_doctor_appointment(doctor_id: int, appointment_id: int):
        return availability_service.cancel_appointment(
            doctor_id=doctor_id, appointment_id=appointment_id
        )

    @app.exception_handler(NotFoundException)
    async def not_found(request: Request, exc: NotFoundException):
        return Response(status_code=404)

    @app.exception_handler(ResoruceAlreadyExistsException)
    async def resource_already_exists(
        request: Request, exc: ResoruceAlreadyExistsException
    ):
        return Response(status_code=409)

    @app.on_event("shutdown")
    def shutdown():
        if db:
            db.close_db()

    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse("/docs")

    return app


app = create_app()
