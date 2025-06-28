from sqlalchemy.orm import Session
from app.models.attendee import Attendee
from app.models.event import Event
from app.schemas.attendee import AttendeeCreate
from fastapi import HTTPException

from app.services.event_service import get_event_by_id

def register_attendee(db: Session, event_id: int, attendee: AttendeeCreate):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    attendees_count = db.query(Attendee).filter(Attendee.event_id == event_id).count()
    if attendees_count >= event.max_capacity:
        raise HTTPException(status_code=400, detail="Event is fully booked")

    existing = db.query(Attendee).filter(
        Attendee.event_id == event_id, Attendee.email == attendee.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already registered")

    new_attendee = Attendee(**attendee.dict(), event_id=event_id)
    db.add(new_attendee)
    db.commit()
    db.refresh(new_attendee)
    return new_attendee

def list_attendees(db: Session, event_id: int, offset: int = 0, limit: int = 10):
    # Will raise 404 if event doesn't exist
    get_event_by_id(db, event_id)

    # Proceed to fetch attendees
    return (db.query(Attendee).filter(Attendee.event_id == event_id).offset(offset).limit(limit).all())
