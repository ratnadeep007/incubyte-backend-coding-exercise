from ast import Dict
from app.database.db import DB
from app.models.doctor import DoctorAppointment, DoctorSchedule
from app.models.error import NotFoundException, ResoruceAlreadyExistsException


class AvailabilityService:
    """
    This is left up to you to implement, generally following the patterns in the repo.

    That said, *don't* feel obliged to make an abstract base class/interface for your chosen approach - you
    can simply write the service using either the database or in-memory approach from the beginning.
    We used that pattern for the doctor_service to have examples for both modes.
    """

    def __init__(self, db: DB):
        self.db = db

    def list_doctor_schedules(self, doctor_id: int) -> list:
        """
        Returns a list of schedules for the given doctor
        """
        dict_result = self.db.execute(
            "SELECT id, doctor_id, location_id, start_time, end_time "
            "FROM doctor_schedules "
            "WHERE doctor_id = ?",
            [doctor_id],
        )

        return [DoctorSchedule(**res) for res in dict_result]

    def create_doctor_schedule(
        self,
        doctor_id: int,
        location_id: int,
        start_time: str,
        end_time: str,
    ) -> int:
        """
        Checks if doctor already have for given location, day and time
        """
        # Check if doctor is availible at given day and time
        dict_result_schedule = self.db.execute(
            "SELECT doctor_id, location_id, start_time, end_time "
            "FROM doctor_schedules "
            "WHERE doctor_id = ?"
            "AND location_id = ?"
            "AND start_time <= ? "
            "AND end_time >= ?",
            [doctor_id, location_id, start_time, end_time],
        )

        if dict_result_schedule:
            raise ResoruceAlreadyExistsException()

        self.db.execute(
            "INSERT INTO doctor_schedules (doctor_id, location_id, start_time, end_time) "
            "VALUES (?, ?, ?, ?)",
            [
                doctor_id,
                location_id,
                start_time,
                end_time,
            ],
        )

        id = self.db.last_row_id

        assert id

        return id

    def list_doctor_appointments(self, doctor_id: int) -> DoctorAppointment:
        """
        Returns an appointment for the given doctor
        """
        dict_result = self.db.execute(
            "SELECT id, doctor_id, location_id, patient_name, time "
            "FROM doctor_appointments "
            "WHERE doctor_id = ?",
            [doctor_id],
        )

        if not dict_result:
            raise NotFoundException()

        return [DoctorAppointment(**res) for res in dict_result]

    def create_appointment(
        self,
        doctor_id: int,
        location_id: int,
        time: str,
        patient_name: str,
    ) -> DoctorAppointment:
        """
        Checks if doctor is availible at given time and creates an appointment
        """
        # Check if doctor is availible at given day and time
        dict_result_schedule = self.db.execute(
            "SELECT doctor_id, location_id, start_time, end_time "
            "FROM doctor_schedules "
            "WHERE doctor_id = ?"
            "AND location_id = ?"
            "AND ? BETWEEN start_time AND end_time",
            [doctor_id, location_id, time],
        )

        if not dict_result_schedule:
            raise NotFoundException()

        # Check doctor has an appointment at given time
        dict_result_appointment = self.db.execute(
            "SELECT doctor_id, location_id, time, is_active "
            "FROM doctor_appointments "
            "WHERE doctor_id = ? "
            "AND location_id = ?"
            "AND time = ?",
            [doctor_id, location_id, time],
        )

        if dict_result_appointment and dict_result_appointment[0]["is_active"]:
            raise ResoruceAlreadyExistsException()

        self.db.execute(
            "INSERT INTO doctor_appointments (doctor_id, location_id, time, patient_name, is_active) "
            "VALUES (?, ?, ?, ?, ?)",
            [doctor_id, location_id, time, patient_name, True],
        )

        id = self.db.last_row_id

        assert id

        return DoctorAppointment(
            id=id,
            doctor_id=doctor_id,
            location_id=location_id,
            time=time,
            patient_name=patient_name,
            is_active=True,
        )

    def cancel_appointment(self, doctor_id: int, appointment_id: int) -> None:
        """
        Cancels an appointment
        """
        self.db.execute(
            "UPDATE doctor_appointments " "SET is_active = ? " "WHERE id = ?",
            [False, appointment_id],
        )
