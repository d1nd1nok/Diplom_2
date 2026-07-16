import allure
import pytest
from src.user_heplers import User


@allure.suite("Изменение данных пользователя")
class TestChangeUserData:

    @allure.title("Изменение данных авторизованным пользователем")
    @allure.description("Авторизованный пользователь может изменить имя, email или пароль — код 200")
    @pytest.mark.parametrize("new_data", ["name", "email", "password"])
    def test_change_user_data(self, authorized_user, new_data):
        payload = authorized_user["payload"]
        access_token = authorized_user["token"]

        payload[new_data] = 'new_' + payload[new_data]

        response_change_data = User().change_data(payload, access_token)

        assert response_change_data.status_code == 200

    @allure.title("Изменение данных без авторизации")
    @allure.description("Изменение данных без токена возвращает 401 и сообщение об ошибке")
    def test_change_user_data_without_authentication(self, registered_user):
        payload = registered_user["payload"]

        payload['name'] = 'new_' + payload['name']

        response_change_data = User().change_data(payload)

        assert response_change_data.status_code == 401
        assert response_change_data.json()["message"] == User.NO_AUTHORIZATION

    @allure.title("Изменение email на уже существующий")
    @allure.description("Смена email на занятый другим пользователем возвращает 403 и сообщение об ошибке")
    def test_change_user_data_to_existing_email(self, authorized_user, registered_user):
        payload1 = authorized_user["payload"]
        access_token = authorized_user["token"]
        payload2 = registered_user["payload"]

        payload1['email'] = payload2['email']

        response_change_data = User().change_data(payload1, access_token)

        assert response_change_data.status_code == 403
        assert response_change_data.json()["message"] == User.EMAIL_EXISTS
