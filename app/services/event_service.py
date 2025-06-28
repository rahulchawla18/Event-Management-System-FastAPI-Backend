from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import pytz

from app.models.event import Event
from app.schemas.event import EventCreate

# Timezones
IST = pytz.timezone("Asia/Kolkata")
UTC = pytz.utc

def to_utc(dt: datetime) -> datetime:
    """
    Convert aware datetime in any timezone to UTC.
    If naive, assume it's in IST and convert to UTC.
    """
    if dt.tzinfo is None:
        dt = IST.localize(dt)
    return dt.astimezone(UTC)

def to_ist(dt: datetime) -> datetime:
    """
    Convert UTC datetime to IST (for display).
    """
    if dt.tzinfo is None:
        dt = UTC.localize(dt)
    return dt.astimezone(IST)

def create_event(db: Session, event: EventCreate) -> Event:
    # Convert input datetimes to UTC before saving
    start_time_utc = to_utc(event.start_time)
    end_time_utc = to_utc(event.end_time)

    # Now check for duplicates using UTC datetime
    existing_event = db.query(Event).filter(
        Event.name == event.name,
        Event.location == event.location,
        Event.start_time == start_time_utc
    ).first()

    if existing_event:
        raise HTTPException(status_code=400, detail="Duplicate event already exists.")

    new_event = Event(
        name=event.name,
        location=event.location,
        start_time=start_time_utc,
        end_time=end_time_utc,
        max_capacity=event.max_capacity,
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def get_upcoming_events(db: Session):
    now_utc = datetime.now(UTC)
    events = db.query(Event).filter(Event.start_time > now_utc).all()
    if not events:
        raise HTTPException(status_code=404, detail="Currently there are no upcoming events.")

    # Convert times to IST for display
    for event in events:
        event.start_time = to_ist(event.start_time)
        event.end_time = to_ist(event.end_time)
    return events

def get_event_by_id(db: Session, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found.")

    # Convert times to IST for display
    event.start_time = to_ist(event.start_time)
    event.end_time = to_ist(event.end_time)
    return event
