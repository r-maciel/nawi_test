import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.models import User  # Asegúrate de ajustar la importación


@pytest.fixture(name="session")
def session_fixture():
    # Base de datos en memoria para pruebas
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
