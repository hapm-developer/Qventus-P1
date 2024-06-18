from typing import List

import pytest
from app.api.deps import get_db
from app.core.settings.app import AppSettings
from app.core.settings.test import TestAppSettings
from app.main import app
from app.models.base import Base
from app.schemas.parts import Part
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


@pytest.fixture(scope="session")
def settings() -> AppSettings:
    return TestAppSettings()


@pytest.fixture(scope="session")
def db_engine(settings: TestAppSettings) -> Engine:
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)  # type: ignore
    yield engine
    Base.metadata.drop_all(bind=engine)  # type: ignore
    engine.dispose()


@pytest.fixture(scope="session")
def db_session(db_engine: Engine) -> Session:
    local_session = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)

    with local_session() as session:
        try:
            yield session
        finally:
            session.close()


@pytest.fixture
def client(db_session: Session) -> TestClient:
    # Override the get_db dependency to use the test database session
    def _get_test_db() -> Session:
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db
    yield TestClient(app)
    app.dependency_overrides[get_db] = get_db


@pytest.fixture
def initialize_data(db_session: Session) -> List[Part]:
    parts = []
    part_data = [
        {
            "name": "Initial Part 1",
            "sku": "SKU0010",
            "description": "Initial Description 1",
            "weight_ounces": 10,
        },
        {
            "name": "Initial Part 2",
            "sku": "SKU0021",
            "description": "Initial Description 2",
            "weight_ounces": 20,
        },
    ]
    for data in part_data:
        part = Part(**data)
        db_session.add(part)
        db_session.refresh(part)
        parts.append(part)
    db_session.commit()

    return parts
