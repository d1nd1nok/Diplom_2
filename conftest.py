import pytest

from src.user_heplers import User


@pytest.fixture
def registered_user():
    """Регистрирует нового пользователя и удаляет его после теста.

    Возвращает dict с исходным payload и токеном (для тестов логина
    и других сценариев, где авторизация не требуется заранее).
    """
    payload = User.valid_user()
    response_register = User().register(payload)
    assert response_register.status_code == 200
    access_token = response_register.json().get("accessToken")

    yield {"payload": payload, "token": access_token}

    User().delete(access_token)


@pytest.fixture
def cleanup_users():
    """Удаляет всех пользователей, чьи токены тест добавит в возвращаемый список.

    Для тестов, где регистрация — это проверяемое поведение (нельзя вынести
    в фикстуру), но созданных пользователей всё равно нужно за собой удалить.
    """
    tokens = []

    yield tokens

    for access_token in tokens:
        if access_token:
            User().delete(access_token)


@pytest.fixture
def authorized_user():
    """Регистрирует и авторизует пользователя, удаляет его после теста.

    Возвращает dict с исходным payload и актуальным токеном авторизации.
    """
    payload = User.valid_user()
    response_register = User().register(payload)
    assert response_register.status_code == 200

    response_login = User().login(payload)
    assert response_login.status_code == 200
    access_token = response_login.json().get("accessToken")
    assert access_token is not None

    yield {"payload": payload, "token": access_token}

    User().delete(access_token)
