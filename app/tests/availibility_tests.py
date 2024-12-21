from fastapi.testclient import TestClient
import pytest

from app.settings import Settings


@pytest.fixture(autouse=True, params=[True, False])
def mode(request) -> None:
    """
    Run all the tests in this file in both in_database and in_memory mode.
    """
    Settings.in_database = request.param


def test_get_all_doctor_schedules(client: TestClient):
    # Test getting all doctor schedules, successfully
    rv = client.get("/doctors/0/schedules")
    assert rv.status_code == 200

    data = rv.json()
    assert len(data) == 1
    assert data[0]["id"] == 0
    assert data[0]["doctor_id"] == 0
    assert data[0]["location_id"] == 0
    assert data[0]["start_time"] == "09:00"
    assert data[0]["end_time"] == "10:00"


def test_create_doctor_schedule(client: TestClient):
    # Test creating a doctor schedule, successfully
    rv = client.post(
        "/doctors/0/schedules",
        json=(dict(location_id=0, start_time="09:00", end_time="10:00")),
    )

    assert rv.status_code == 200

    data = rv.json()
    assert data["id"] == 1


def test_get_all_doctor_appointments(client: TestClient):
    # Test getting all doctor appointments, successfully
    rv = client.get("/doctors/0/appointments")
    assert rv.status_code == 200

    data = rv.json()
    assert len(data) == 1
    assert data[0]["id"] == 0
    assert data[0]["doctor_id"] == 0
    assert data[0]["location_id"] == 0
    assert data[0]["time"] == "09:00"
    assert data[0]["patient_name"] == "Jane"
    assert data[0]["is_active"] == True


def test_create_doctor_appointment(client: TestClient):
    # Test creating a doctor appointment, successfully
    rv = client.post(
        "/doctors/0/appointments",
        json=(dict(location_id=0, time="09:00", patient_name="Jane")),
    )

    assert rv.status_code == 200

    data = rv.json()
    assert data["id"] == 0


def test_cancel_doctor_appointment(client: TestClient):
    # Test canceling a doctor appointment, successfully
    rv = client.delete("/doctors/0/appointments/0")  # doctor_id=0, appointment_id=0
    assert rv.status_code == 200

    data = rv.json()
    assert data["id"] == 0
