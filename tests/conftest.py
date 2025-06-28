import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_TEST_DB_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# override dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# create test DB tables
Base.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    return TestClient(app)
