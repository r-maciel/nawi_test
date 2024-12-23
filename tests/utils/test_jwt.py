import pytest
from datetime import timedelta, datetime, timezone
from unittest.mock import MagicMock
import jwt
from app.utils.jwt import (
    get_access_token,
    get_refresh_token,
    create_access_token,
    decode_access_token,
    validate_token
)
from app.models import RevokedToken
from sqlmodel import SQLModel, create_engine, Session
from fastapi import HTTPException
from app.settings import settings


def test_get_access_token(mock_settings):
    data = {"sub": "test_user"}
    token = get_access_token(data)

    decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])

    assert decoded["sub"] == "test_user"
    assert "exp" in decoded


def test_get_refresh_token(mock_settings):
    data = {"sub": "test_user"}
    token = get_refresh_token(data)

    decoded = jwt.decode(token, settings.jwt_refresh_secret_key, algorithms=["HS256"])
    assert decoded["sub"] == "test_user"
    assert "exp" in decoded


def test_create_access_token(mock_settings):
    data = {"sub": "test_user"}
    expires_delta = timedelta(minutes=5)
    token = create_access_token(data, expires_delta, settings.jwt_secret_key)

    decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
    assert decoded["sub"] == "test_user"
    assert "exp" in decoded

    expected_exp = datetime.now(timezone.utc) + expires_delta
    assert decoded["exp"] == int(expected_exp.timestamp())


def test_decode_valid_token(mock_settings):
    data = {"sub": "test_user"}
    token = create_access_token(data, timedelta(minutes=5), settings.jwt_secret_key)

    decoded = decode_access_token(token, settings.jwt_secret_key)
    assert decoded["sub"] == "test_user"


def test_decode_expired_token(mock_settings):
    data = {"sub": "test_user"}
    token = create_access_token(data, timedelta(seconds=-1), settings.jwt_secret_key)

    decoded = decode_access_token(token, settings.jwt_secret_key)
    assert decoded is None


def test_validate_valid_token(mock_settings, session):
    data = {"sub": "test_user"}
    token = create_access_token(data, timedelta(minutes=5), "test_secret_key")

    decoded = validate_token(token, "test_secret_key", session)
    assert decoded["sub"] == "test_user"


def test_validate_revoked_token(mock_settings, session):
    data = {"sub": "test_user"}
    token = create_access_token(data, timedelta(minutes=5), "test_secret_key")

    revoked_token = RevokedToken(token=token)
    session.add(revoked_token)
    session.commit()

    with pytest.raises(HTTPException) as error:
        validate_token(token, "test_secret_key", session)
    assert error.value.status_code == 401
    assert error.value.detail == "Token has been revoked"
