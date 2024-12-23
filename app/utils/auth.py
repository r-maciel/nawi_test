from passlib.context import CryptContext


_PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return _PWD_CONTEXT.hash(password)


def verify_password(plain_password, hashed_password):
    return _PWD_CONTEXT.verify(plain_password, hashed_password)
