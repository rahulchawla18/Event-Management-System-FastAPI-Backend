from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.attendee import AttendeeCreate, AttendeeOut
from app.services.attendee_service import register_attendee, list_attendees

router = APIRouter(prefix="/events/{event_id}", tags=["Attendees"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=AttendeeOut)
def register(event_id: int, attendee: AttendeeCreate, db: Session = Depends(get_db)):
    return register_attendee(db, event_id, attendee)

@router.get("/attendees", response_model=list[AttendeeOut])
def get_attendees(
    event_id: int,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    return list_attendees(db, event_id, offset, limit)
