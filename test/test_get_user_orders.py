import allure
import requests
from src.user_heplers import User
from src.order_helpers import Order
from src.urls import CREATE_ORDERS, REGISTER, LOGIN, USER_DATA


@allure.suite("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованным пользователем")
    @allure.description("Авторизованный пользователь получает список своих заказов с кодом 200")
    def test_get_user_orders_with_authentication(self):
        with allure.step("Зарегистрировать нового пользователя"):
            payload = User.valid_user()
            response_register = requests.post(REGISTER, data=payload)
            assert response_register.status_code == 200

        with allure.step("Авторизоваться и получить токен"):
            response_login = requests.post(LOGIN, data=payload)
            assert response_login.status_code == 200
            access_token = response_login.json().get("accessToken")
            assert access_token is not None

        with allure.step("Создать заказ для пользователя"):
            headers = {'Authorization': str(access_token)}
            payload_ingredients = {"ingredients": Order.valid_ingredients()}
            requests.post(CREATE_ORDERS, headers=headers, data=payload_ingredients)

        with allure.step("Запросить заказы пользователя с токеном"):
            response = requests.get(CREATE_ORDERS, headers=headers)

        with allure.step("Проверить, что вернулся список заказов"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert isinstance(response.json()["orders"], list)

        with allure.step("Удалить созданного пользователя"):
            response_delete = requests.delete(USER_DATA, headers={"Authorization": str(access_token)})
            assert response_delete.status_code == 202
            assert response_delete.json()["success"] is True
            assert response_delete.json()["message"] == User.SUCCESSFULLY_REMOVED

    @allure.title("Получение заказов неавторизованным пользователем")
    @allure.description("Запрос заказов без токена возвращает 401 и сообщение об ошибке")
    def test_get_user_orders_without_authentication(self):
        with allure.step("Запросить заказы без токена авторизации"):
            response = requests.get(CREATE_ORDERS)

        with allure.step("Проверить код ответа 401 и текст ошибки"):
            assert response.status_code == 401
            assert response.json()["message"] == User.NO_AUTHORIZATION
