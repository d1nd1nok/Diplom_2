import allure
import requests
from src.urls import REGISTER, USER_DATA
from src.user_heplers import User
import pytest


@allure.suite("Регистрация пользователя")
class TestRegisterUser:

    @allure.title("Успешная регистрация пользователя")
    @allure.description("Регистрация с валидными данными возвращает код 200")
    def test_register_user_success(self):
        with allure.step("Зарегистрировать пользователя с валидными данными"):
            payload = User.valid_user()
            response = requests.post(REGISTER, data=payload)

        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200

        with allure.step("Удалить созданного пользователя"):
            access_token = response.json().get("accessToken")
            response_delete = requests.delete(USER_DATA, headers={"Authorization": str(access_token)})
            assert response_delete.status_code == 202
            assert response_delete.json()["success"] is True
            assert response_delete.json()["message"] == User.SUCCESSFULLY_REMOVED

    @allure.title("Регистрация пользователя с уже существующим email")
    @allure.description("Повторная регистрация того же пользователя возвращает 403 и сообщение об ошибке")
    def test_register_user_with_existing_email(self):
        with allure.step("Зарегистрировать пользователя"):
            payload = User.valid_user()
            response = requests.post(REGISTER, data=payload)
            assert response.status_code == 200

        with allure.step("Повторно зарегистрировать того же пользователя"):
            response_existing_email = requests.post(REGISTER, data=payload)

        with allure.step("Проверить код ответа 403 и текст ошибки"):
            assert response_existing_email.status_code == 403
            assert response_existing_email.json()["message"] == User.ALREADY_EXISTS

        with allure.step("Удалить созданного пользователя"):
            access_token = response.json().get("accessToken")
            response_delete = requests.delete(USER_DATA, headers={"Authorization": str(access_token)})
            assert response_delete.status_code == 202
            assert response_delete.json()["success"] is True
            assert response_delete.json()["message"] == User.SUCCESSFULLY_REMOVED

    @allure.title("Регистрация пользователя без обязательного поля")
    @allure.description("Регистрация без одного из обязательных полей возвращает 403 и сообщение об ошибке")
    @pytest.mark.parametrize("missing_field", ["name", "email", "password"])
    def test_register_user_with_missing_fields(self, missing_field):
        with allure.step(f"Убрать обязательное поле '{missing_field}' из данных"):
            payload = User.valid_user()
            del payload[missing_field]

        with allure.step("Зарегистрировать пользователя без обязательного поля"):
            response = requests.post(REGISTER, data=payload)

        with allure.step("Проверить код ответа 403 и текст ошибки"):
            assert response.status_code == 403
            assert response.json()["message"] == User.MISSING_FIELDS
