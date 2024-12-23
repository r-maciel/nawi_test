from app.models.user import User


def test_user_initialization():
    user = User(name="Homer Simpson", username="homers", password="password")
    assert user.name == "Homer Simpson"
    assert user.username == "homers"
    assert user.password == "password"


def test_create_user(session):
    user = User(name="Homer Simpson", username="homers", password="password")
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.name == "Homer Simpson"
    assert user.username == "homers"
