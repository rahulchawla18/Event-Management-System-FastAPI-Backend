import pytest

from datetime import datetime, timedelta

@pytest.fixture
def create_event(client):
    def _create_event(name="Test Event", max_capacity=3):
        response = client.post("/events/", json={
            "name": name,
            "location": "Test Location",
            "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
            "end_time": (datetime.now() + timedelta(days=2)).isoformat(),
            "max_capacity": max_capacity
        })
        assert response.status_code == 200
        return response.json()
    return _create_event


def test_create_event(client):
    response = client.post("/events/", json={
        "name": "Launch Party",
        "location": "Delhi",
        "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(days=1, hours=3)).isoformat(),
        "max_capacity": 5
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_create_duplicate_event(client):
    event_data = {
        "name": "Duplicate Test Event",
        "location": "Test City",
        "start_time": "2025-06-30T10:00:00+05:30",
        "end_time": "2025-06-30T12:00:00+05:30",
        "max_capacity": 50
    }
    response1 = client.post("/events/", json=event_data)
    assert response1.status_code == 200

    response2 = client.post("/events/", json=event_data)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Duplicate event already exists."

def test_get_events_list(client, create_event):
    create_event()
    response = client.get("/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_upcoming_events(client, create_event):
    create_event()
    response = client.get("/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_register_attendee_valid(client, create_event):
    event = create_event(name="Valid Event", max_capacity=5)
    response = client.post(f"/events/{event['id']}/register", json={
        "name": "Alice",
        "email": "alice@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"


def test_register_duplicate_attendee(client, create_event):
    event = create_event(name="Duplicate Event", max_capacity=5)
    # First registration
    client.post(f"/events/{event['id']}/register", json={
        "name": "Bob",
        "email": "bob@example.com"
    })
    # Second registration with same email
    response = client.post(f"/events/{event['id']}/register", json={
        "name": "Bob",
        "email": "bob@example.com"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Already registered"


def test_register_attendee_overbooking(client, create_event):
    event = create_event(name="Full Event", max_capacity=1)
    # Fill the event
    client.post(f"/events/{event['id']}/register", json={
        "name": "Charlie",
        "email": "charlie@example.com"
    })
    # Attempt overbooking
    response = client.post(f"/events/{event['id']}/register", json={
        "name": "Dave",
        "email": "dave@example.com"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Event is fully booked"


def test_register_attendee_invalid_event(client):
    response = client.post("/events/999/register", json={
        "name": "Ghost",
        "email": "ghost@example.com"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


def test_list_attendees_valid_event(client, create_event):
    event = create_event(name="List Attendees Event", max_capacity=3)
    client.post(f"/events/{event['id']}/register", json={
        "name": "Kunal",
        "email": "kunal@example.com"
    })
    client.post(f"/events/{event['id']}/register", json={
        "name": "Paras",
        "email": "paras@example.com"
    })
    response = client.get(f"/events/{event['id']}/attendees?limit=10&offset=0")
    assert response.status_code == 200
    attendees = response.json()
    assert isinstance(attendees, list)
    assert len(attendees) == 2


def test_get_event_by_invalid_id(client):
    response = client.get("/events/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event with id 999 not found."