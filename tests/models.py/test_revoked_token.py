from datetime import datetime
from app.models.revoked_token import RevokedToken


def test_revoked_token_initialization():
    token_value = "test_token"
    token = RevokedToken(token=token_value)

    assert token.token == token_value
    assert token.id is None
    assert isinstance(token.revoked_at, datetime)
    assert token.revoked_at <= datetime.utcnow()


def test_create_revoked_token(session):
    token_value = "unique_token"
    token = RevokedToken(token=token_value)
    session.add(token)
    session.commit()
    session.refresh(token)

    assert token.id is not None
    assert token.token == token_value
    assert isinstance(token.revoked_at, datetime)
