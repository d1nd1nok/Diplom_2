import allure
import requests
from faker import Faker

from src.urls import REGISTER, LOGIN, USER_DATA


class User:

    MISSING_FIELDS = "Email, password and name are required fields"
    ALREADY_EXISTS = "User already exists"
    NO_AUTHORIZATION = "You should be authorised"
    EMAIL_EXISTS = "User with such email already exists"
    INVALID_CREDENTIALS = "email or password are incorrect"
    SUCCESSFULLY_REMOVED = "User successfully removed"

    @staticmethod
    def valid_user():
        fake = Faker()

        name = fake.first_name()
        email = fake.email()
        password = fake.password()

        return {
            "name": name,
            "email": email,
            "password": password
        }

    @allure.step("Зарегистрировать пользователя")
    def register(self, payload):
        return requests.post(REGISTER, data=payload)

    @allure.step("Авторизовать пользователя")
    def login(self, payload):
        return requests.post(LOGIN, data=payload)

    @allure.step("Изменить данные пользователя")
    def change_data(self, payload, access_token=None):
        headers = {"Authorization": str(access_token)} if access_token else None
        return requests.patch(USER_DATA, headers=headers, data=payload)

    @allure.step("Удалить пользователя")
    def delete(self, access_token):
        return requests.delete(USER_DATA, headers={"Authorization": str(access_token)})
