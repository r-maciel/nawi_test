from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.exc import IntegrityError
from app.db import SessionDep
from app.models.user import User
from app.utils.auth import hash_password
from app.exceptions import UserIntegrityException

router = APIRouter(prefix="/users")


@router.post("/")
def register_user(user: User, session: SessionDep) -> dict:
    user.id = None
    user.password = hash_password(user.password)

    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise UserIntegrityException(
            status_code=400,
            detail="Username is already taken."
        )

    return {"message": "User created successfully"}
