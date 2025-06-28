from fastapi import APIRouter, Depends, HTTPException, Query
import pytz
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.event import EventCreate, EventOut
from app.services.event_service import create_event, get_event_by_id, get_upcoming_events

router = APIRouter(prefix="/events", tags=["Events"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EventOut)
def create_event_api(event: EventCreate, db: Session = Depends(get_db)):
    return create_event(db, event)

@router.get("/", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db), timezone: str = Query("Asia/Kolkata")):
    events = get_upcoming_events(db)
    try:
        target_tz = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        raise HTTPException(status_code=400, detail="Invalid timezone")

    for event in events:
        event.start_time = event.start_time.astimezone(target_tz)
        event.end_time = event.end_time.astimezone(target_tz)
    return events

@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    return get_event_by_id(db, event_id)
