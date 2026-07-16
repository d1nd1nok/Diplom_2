import allure
from src.user_heplers import User
import pytest


@allure.suite("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Успешная авторизация пользователя")
    @allure.description("Авторизация зарегистрированного пользователя возвращает код 200")
    def test_login_user(self, registered_user):
        payload = registered_user["payload"]

        response_login = User().login(payload)

        assert response_login.status_code == 200

    @allure.title("Авторизация с неверными данными")
    @allure.description("Авторизация с неверным email или паролем возвращает 401 и сообщение об ошибке")
    @pytest.mark.parametrize("invalid_field", ["email", "password"])
    def test_login_user_with_invalid_credentials(self, registered_user, invalid_field):
        payload = registered_user["payload"]

        payload[invalid_field] = 'invalid_' + invalid_field

        response_login = User().login(payload)

        assert response_login.status_code == 401
        assert response_login.json()["message"] == User.INVALID_CREDENTIALS
