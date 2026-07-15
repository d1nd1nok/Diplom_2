import allure
import requests

from src.urls import INGREDIENTS, CREATE_ORDERS


class Order:
    MISSING_INGREDIENTS = "Ingredient ids must be provided"
    INVALID_HASH = "invalid_ingredient_hash"

    @allure.step("Получить список ингредиентов")
    def get_ingredients(self):
        return requests.get(INGREDIENTS)

    def valid_ingredients(self, count=2):
        response = self.get_ingredients()
        data = response.json()["data"]
        return [item["_id"] for item in data[:count]]

    @allure.step("Создать заказ")
    def create_order(self, ingredients, access_token=None):
        headers = {"Authorization": str(access_token)} if access_token else None
        return requests.post(CREATE_ORDERS, headers=headers, data={"ingredients": ingredients})

    @allure.step("Получить заказы пользователя")
    def get_orders(self, access_token=None):
        headers = {"Authorization": str(access_token)} if access_token else None
        return requests.get(CREATE_ORDERS, headers=headers)
