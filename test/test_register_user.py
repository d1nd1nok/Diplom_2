import allure
from src.user_heplers import User
import pytest


@allure.suite("Регистрация пользователя")
class TestRegisterUser:

    @allure.title("Успешная регистрация пользователя")
    @allure.description("Регистрация с валидными данными возвращает код 200")
    def test_register_user_success(self, cleanup_users):
        payload = User.valid_user()
        response = User().register(payload)

        cleanup_users.append(response.json().get("accessToken"))

        assert response.status_code == 200

    @allure.title("Регистрация пользователя с уже существующим email")
    @allure.description("Повторная регистрация того же пользователя возвращает 403 и сообщение об ошибке")
    def test_register_user_with_existing_email(self, cleanup_users):
        payload = User.valid_user()
        response = User().register(payload)

        cleanup_users.append(response.json().get("accessToken"))

        response_existing_email = User().register(payload)

        assert response_existing_email.status_code == 403
        assert response_existing_email.json()["message"] == User.ALREADY_EXISTS

    @allure.title("Регистрация пользователя без обязательного поля")
    @allure.description("Регистрация без одного из обязательных полей возвращает 403 и сообщение об ошибке")
    @pytest.mark.parametrize("missing_field", ["name", "email", "password"])
    def test_register_user_with_missing_fields(self, missing_field):
        payload = User.valid_user()
        del payload[missing_field]

        response = User().register(payload)

        assert response.status_code == 403
        assert response.json()["message"] == User.MISSING_FIELDS
