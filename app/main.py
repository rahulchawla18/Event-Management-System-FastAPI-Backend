from fastapi import FastAPI
from app.routes import event_routes, attendee_routes
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management System")

app.include_router(event_routes.router)
app.include_router(attendee_routes.router)
