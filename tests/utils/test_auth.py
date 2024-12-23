from app.utils.auth import hash_password, verify_password


def test_hash_password():
    password = "password"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert len(hashed_password) > 0


def test_hash_password_is_unique():
    password = "password"
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2


def test_verify_password_correct():
    password = "password"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password)


def test_verify_password_incorrect():
    password = "password"
    hashed_password = hash_password(password)

    assert not verify_password("wrongpassword", hashed_password)
