from hesma.users.models import User
from hesma.users.tests.factories import UserFactory


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_user_factory_saves_postgenerated_password(db):
    user = UserFactory(password="test-password")
    user.refresh_from_db()
    assert user.check_password("test-password")
