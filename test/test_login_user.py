import allure
from src.user_heplers import User
from src.urls import REGISTER, LOGIN, USER_DATA
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

        with allure.step("Удалить созданного пользователя"):
            access_token = response_register.json().get("accessToken")
            response_delete = requests.delete(USER_DATA, headers={"Authorization": str(access_token)})
            assert response_delete.status_code == 202
            assert response_delete.json()["success"] is True
            assert response_delete.json()["message"] == User.SUCCESSFULLY_REMOVED

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

        with allure.step("Удалить созданного пользователя"):
            access_token = response_register.json().get("accessToken")
            response_delete = requests.delete(USER_DATA, headers={"Authorization": str(access_token)})
            assert response_delete.status_code == 202
            assert response_delete.json()["success"] is True
            assert response_delete.json()["message"] == User.SUCCESSFULLY_REMOVED
