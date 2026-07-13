import allure
from src.user_heplers import User
from src.urls import REGISTER, LOGIN
import requests
import pytest


@allure.suite("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Успешная авторизация пользователя")
    @allure.description("Авторизация зарегистрированного пользователя возвращает код 200")
    def test_login_user(self):
        with allure.step("Зарегистрировать пользователя"):
            payload = User.valid_user()
            response_register = requests.post(REGISTER, data=payload)
            assert response_register.status_code == 200

        with allure.step("Авторизоваться с валидными данными"):
            response_login = requests.post(LOGIN, data=payload)

        with allure.step("Проверить код ответа 200"):
            assert response_login.status_code == 200

    @allure.title("Авторизация с неверными данными")
    @allure.description("Авторизация с неверным email или паролем возвращает 401 и сообщение об ошибке")
    @pytest.mark.parametrize("invalid_field", ["email", "password"])
    def test_login_user_with_invalid_credentials(self, invalid_field):
        with allure.step("Зарегистрировать пользователя"):
            payload = User.valid_user()
            response_register = requests.post(REGISTER, data=payload)
            assert response_register.status_code == 200

        with allure.step(f"Испортить поле '{invalid_field}' и авторизоваться"):
            payload[invalid_field] = 'invalid_' + invalid_field
            response_login = requests.post(LOGIN, data=payload)

        with allure.step("Проверить код ответа 401 и текст ошибки"):
            assert response_login.status_code == 401
            assert response_login.json()["message"] == User.INVALID_CREDENTIALS
