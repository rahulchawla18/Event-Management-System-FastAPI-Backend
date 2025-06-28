from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from app.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    max_capacity = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('name', 'location', 'start_time', name='uq_event_name_location_start'),
    )