import allure
import requests
from src.user_heplers import User
from src.order_helpers import Order
from src.urls import CREATE_ORDERS, REGISTER, LOGIN, USER_DATA


@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа авторизованным пользователем")
    @allure.description("Заказ с валидными ингредиентами и токеном авторизации возвращает 200 и номер заказа")
    def test_create_order_with_authentication(self):
        with allure.step("Зарегистрировать нового пользователя"):
            payload = User.valid_user()
            response_register = requests.post(REGISTER, data=payload)
            assert response_register.status_code == 200

        with allure.step("Авторизоваться и получить токен"):
            response_login = requests.post(LOGIN, data=payload)
            assert response_login.status_code == 200
            access_token = response_login.json().get("accessToken")
            assert access_token is not None

        with allure.step("Создать заказ с ингредиентами и токеном"):
            headers = {'Authorization': str(access_token)}
            payload_ingredients = {"ingredients": Order.valid_ingredients()}
            response = requests.post(CREATE_ORDERS, headers=headers, data=payload_ingredients)

        with allure.step("Проверить, что заказ создан и вернулся его номер"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert response.json()["order"]["number"] is not None

        with allure.step("Удалить созданного пользователя"):
            response_delete = requests.delete(USER_DATA, headers={"Authorization": str(access_token)})
            assert response_delete.status_code == 202
            assert response_delete.json()["success"] is True
            assert response_delete.json()["message"] == User.SUCCESSFULLY_REMOVED

    @allure.title("Создание заказа без авторизации")
    @allure.description("Заказ с валидными ингредиентами без токена возвращает 200")
    def test_create_order_without_authentication(self):
        with allure.step("Создать заказ с ингредиентами без токена"):
            payload_ingredients = {"ingredients": Order.valid_ingredients()}
            response = requests.post(CREATE_ORDERS, data=payload_ingredients)

        with allure.step("Проверить, что заказ создан"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Создание заказа с ингредиентами")
    @allure.description("Заказ с валидными хешами ингредиентов возвращает 200")
    def test_create_order_with_ingredients(self):
        with allure.step("Создать заказ с валидными ингредиентами"):
            payload_ingredients = {"ingredients": Order.valid_ingredients()}
            response = requests.post(CREATE_ORDERS, data=payload_ingredients)

        with allure.step("Проверить, что заказ создан"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Заказ с пустым списком ингредиентов возвращает 400 и сообщение об ошибке")
    def test_create_order_without_ingredients(self):
        with allure.step("Создать заказ с пустым списком ингредиентов"):
            payload_ingredients = {"ingredients": []}
            response = requests.post(CREATE_ORDERS, data=payload_ingredients)

        with allure.step("Проверить код ответа 400 и текст ошибки"):
            assert response.status_code == 400
            assert response.json()["message"] == Order.MISSING_INGREDIENTS

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.description("Заказ с невалидным хешем ингредиента возвращает 500 Internal Server Error")
    def test_create_order_with_invalid_ingredient_hash(self):
        with allure.step("Создать заказ с невалидным хешем ингредиента"):
            payload_ingredients = {"ingredients": [Order.INVALID_HASH]}
            response = requests.post(CREATE_ORDERS, data=payload_ingredients)

        with allure.step("Проверить код ответа 500"):
            assert response.status_code == 500
