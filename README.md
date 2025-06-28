# Event-Management-System-FastAPI-Backend

A Mini Event Management System built using **FastAPI**, **SQLAlchemy**, and **SQLite**. This backend allows users to create events, register attendees, and retrieve upcoming events while following best practices like UTC storage for datetime and graceful error handling.

---

## 🌐 Features

- **Create Events** with unique name, location, start time and end time
- **Timezone-aware Event Listings** – convert times from UTC to user's timezone
- **Register Attendees** to events (ensuring no duplicates)
- **Paginated Attendee Lists**
- **Duplicate Event Validation**
- **Datetime stored in UTC**, displayed in user-defined timezone
- Clean and modular project structure with **Pydantic**, **SQLAlchemy**, and **FastAPI**

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/rahulchawla18/Event-Management-System-FastAPI-Backend.git
cd Event-Management-System-FastAPI-Backend
```

### 2. Create Virtual Environment & Install Dependencies

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt


### 3. Run the Application

uvicorn app.main:app --reload
Access Swagger UI at: http://localhost:8000/docs

---

## API Endpoints

1. Create Event
    - POST /events/
    - Payload: {
                    "name": "Django Meetup",
                    "location": "Bangalore",
                    "start_time": "2025-06-30T10:00:00+05:30",
                    "end_time": "2025-06-30T12:00:00+05:30",
                    "max_capacity": 50
                }

2. List All Events (Upcoming)
    - GET /events/
    - Optional Query Param: ?timezone=Asia/Kolkata
    - Response: [
                    {
                        "id": 1,
                        "name": "Django Meetup",
                        "location": "Bangalore",
                        "start_time": "2025-06-30T10:00:00+05:30",
                        "end_time": "2025-06-30T12:00:00+05:30",
                        "max_capacity": 50
                    }
                ]

3. Get Event by ID
    - GET /events/{event_id} 

4. Register Attendee
    - POST /events/{event_id}/register
    - Payload: {
                    "name": "John Doe",
                    "email": "john@example.com"
                }
    - Error Scenarios:
        - 400 if attendee already registered
        - 400 if event is full
        - 404 if event does not exist

5. List Attendees
    - GET /events/{event_id}/attendees
    - Query Params:
        - limit (default: 10)
        - offset (default: 0)

---

## Running Tests

- pytest -v tests/test_events.py

## Test coverage includes

- Event creation
- Duplicate event validation
- Attendee registration (valid, duplicate, overbooked)
- Event and attendee fetching