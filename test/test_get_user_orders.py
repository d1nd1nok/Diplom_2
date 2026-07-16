import allure
from src.user_heplers import User
from src.order_helpers import Order


@allure.suite("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованным пользователем")
    @allure.description("Авторизованный пользователь получает список своих заказов с кодом 200")
    def test_get_user_orders_with_authentication(self, authorized_user):
        access_token = authorized_user["token"]

        order = Order()
        order.create_order(order.valid_ingredients(), access_token)
        response = order.get_orders(access_token)

        assert response.status_code == 200
        assert isinstance(response.json()["orders"], list)

    @allure.title("Получение заказов неавторизованным пользователем")
    @allure.description("Запрос заказов без токена возвращает 401 и сообщение об ошибке")
    def test_get_user_orders_without_authentication(self):
        response = Order().get_orders()

        assert response.status_code == 401
        assert response.json()["message"] == User.NO_AUTHORIZATION
