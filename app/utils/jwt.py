from datetime import datetime, timedelta, timezone

import jwt
from app.settings import settings

ACCESS_TOKEN_EXPIRE_MINUTES = 1  # 2 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 3  # 5 days
ALGORITHM = "HS256"


def get_access_token(data: dict) -> str:
    return create_access_token(
        data=data,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        secret_key=settings.jwt_secret_key
    )


def get_refresh_token(data: dict) -> str:
    return create_access_token(
        data=data,
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
        secret_key=settings.jwt_refresh_secret_key
    )


def create_access_token(
    data: dict, expires_delta: timedelta, secret_key: str
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str, secret_key: str) -> str | None:
    try:
        decoded_token = jwt.decode(
            token, secret_key, algorithms=[ALGORITHM]
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
