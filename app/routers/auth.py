from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select
from app.db import SessionDep
from app.models import User, RevokedToken
from app.utils.auth import verify_password
from app.utils.jwt import (
    get_access_token, get_refresh_token, validate_token
)
from app.settings import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/login")
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return {
        "access_token": get_access_token({"sub": user.email}),
        "refresh_token": get_refresh_token({"sub": user.email}),
        "token_type": "bearer"
    }


@router.post("/verify")
def verify_access_token(access_token: str, session: SessionDep):
    decoded_token = validate_token(
        access_token, settings.jwt_secret_key, session
    )

    return {"message": "Token is valid", "username": decoded_token["sub"]}


@router.post("/refresh")
def refresh_token(refresh_token: str, session: SessionDep):
    decoded_token = validate_token(
        refresh_token, settings.jwt_refresh_secret_key, session
    )

    username = decoded_token.get("sub")
    new_access_token = get_access_token(data={"sub": username})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@router.post("/logout", description="Log Out revoking access token")
def logout(access_token: str, session: SessionDep):
    validate_token(
        access_token, settings.jwt_secret_key, session
    )

    revoked_token = RevokedToken(token=access_token)
    session.add(revoked_token)
    session.commit()

    return {"message": "Successfully logged out"}
