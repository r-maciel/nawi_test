import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.models import User, RevokedToken
from app.settings import settings


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def mock_settings(monkeypatch):
    """Simula los valores de configuración en settings."""
    monkeypatch.setattr("app.settings.settings.jwt_secret_key", "test_secret_key")
    monkeypatch.setattr("app.settings.settings.jwt_refresh_secret_key", "test_refresh_secret_key")
    return "test_secret_key", "test_refresh_secret_key"
