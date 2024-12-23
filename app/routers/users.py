from fastapi import APIRouter
from app.db import SessionDep
from app.models.user import User
from app.utils.auth import hash_password

router = APIRouter(prefix="/users")


@router.post("/")
def register_user(user: User, session: SessionDep) -> dict:
    user.id = None
    user.password = hash_password(user.password)
    session.add(user)
    session.commit()

    return {"message": "User created successfully"}
