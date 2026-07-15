import allure
from src.order_helpers import Order


@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа авторизованным пользователем")
    @allure.description("Заказ с валидными ингредиентами и токеном авторизации возвращает 200 и номер заказа")
    def test_create_order_with_authentication(self, authorized_user):
        access_token = authorized_user["token"]

        order = Order()
        response = order.create_order(order.valid_ingredients(), access_token)

        assert response.status_code == 200
        assert response.json()["order"]["number"] is not None

    @allure.title("Создание заказа без авторизации")
    @allure.description("Заказ с валидными ингредиентами без токена возвращает 200")
    def test_create_order_without_authentication(self):
        order = Order()
        response = order.create_order(order.valid_ingredients())

        assert response.status_code == 200

    @allure.title("Создание заказа с ингредиентами")
    @allure.description("Заказ с валидными хешами ингредиентов возвращает 200")
    def test_create_order_with_ingredients(self):
        order = Order()
        response = order.create_order(order.valid_ingredients())

        assert response.status_code == 200

    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Заказ с пустым списком ингредиентов возвращает 400 и сообщение об ошибке")
    def test_create_order_without_ingredients(self):
        response = Order().create_order([])

        assert response.status_code == 400
        assert response.json()["message"] == Order.MISSING_INGREDIENTS

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.description("Заказ с невалидным хешем ингредиента возвращает 500 Internal Server Error")
    def test_create_order_with_invalid_ingredient_hash(self):
        response = Order().create_order([Order.INVALID_HASH])

        assert response.status_code == 500
