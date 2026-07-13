import allure
import requests
import pytest
from src.user_heplers import User
from src.urls import REGISTER, LOGIN, USER_DATA


@allure.suite("Изменение данных пользователя")
class TestChangeUserData:

    @allure.title("Изменение данных авторизованным пользователем")
    @allure.description("Авторизованный пользователь может изменить имя, email или пароль — код 200")
    @pytest.mark.parametrize("new_data", ["name", "email", "password"])
    def test_change_user_data(self, new_data):
        with allure.step("Зарегистрировать пользователя"):
            payload = User.valid_user()
            response_register = requests.post(REGISTER, data=payload)
            assert response_register.status_code == 200

        with allure.step("Авторизоваться и получить токен"):
            response_login = requests.post(LOGIN, data=payload)
            assert response_login.status_code == 200
            access_token = response_login.json().get("accessToken")
            assert access_token is not None

        with allure.step(f"Изменить поле '{new_data}' с токеном авторизации"):
            payload[new_data] = 'new_' + payload[new_data]
            headers = {'Authorization': str(access_token)}
            response_change_data = requests.patch(USER_DATA, headers=headers, data=payload)

        with allure.step("Проверить код ответа 200"):
            assert response_change_data.status_code == 200

    @allure.title("Изменение данных без авторизации")
    @allure.description("Изменение данных без токена возвращает 401 и сообщение об ошибке")
    def test_change_user_data_without_authentication(self):
        with allure.step("Зарегистрировать пользователя"):
            payload = User.valid_user()
            response_register = requests.post(REGISTER, data=payload)
            assert response_register.status_code == 200

        with allure.step("Изменить данные без токена авторизации"):
            payload['name'] = 'new_' + payload['name']
            response_change_data = requests.patch(USER_DATA, data=payload)

        with allure.step("Проверить код ответа 401 и текст ошибки"):
            assert response_change_data.status_code == 401
            assert response_change_data.json()["message"] == User.NO_AUTHORIZATION

    @allure.title("Изменение email на уже существующий")
    @allure.description("Смена email на занятый другим пользователем возвращает 403 и сообщение об ошибке")
    def test_change_user_data_to_existing_email(self):
        with allure.step("Зарегистрировать первого пользователя"):
            payload1 = User.valid_user()
            response_register1 = requests.post(REGISTER, data=payload1)
            assert response_register1.status_code == 200

        with allure.step("Зарегистрировать второго пользователя"):
            payload2 = User.valid_user()
            response_register2 = requests.post(REGISTER, data=payload2)
            assert response_register2.status_code == 200

        with allure.step("Авторизоваться первым пользователем и получить токен"):
            response_login = requests.post(LOGIN, data=payload1)
            assert response_login.status_code == 200
            access_token = response_login.json().get("accessToken")
            assert access_token is not None

        with allure.step("Сменить email первого пользователя на email второго"):
            payload1['email'] = payload2['email']
            headers = {'Authorization': str(access_token)}
            response_change_data = requests.patch(USER_DATA, headers=headers, data=payload1)

        with allure.step("Проверить код ответа 403 и текст ошибки"):
            assert response_change_data.status_code == 403
            assert response_change_data.json()["message"] == User.EMAIL_EXISTS
