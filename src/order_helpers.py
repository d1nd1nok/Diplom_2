import requests
from src.urls import INGREDIENTS


class Order:
    MISSING_INGREDIENTS = "Ingredient ids must be provided"
    INVALID_HASH = "invalid_ingredient_hash"

    @staticmethod
    def valid_ingredients(count=2):
        response = requests.get(INGREDIENTS)
        data = response.json()["data"]
        return [item["_id"] for item in data[:count]]
