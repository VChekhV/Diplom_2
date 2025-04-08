import requests
import random
import string
from faker import Faker
from random import randint, choice
from data import UrlList

# создание пользователя
def generate_user():
    fake = Faker(["ru_RU"])

    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # генерируем логин, пароль и имя пользователя
    email = fake.ascii_email()
    password = generate_random_string(10)
    name =  fake.first_name(),

    # собираем тело запроса
    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    return payload

def generate_order():
    ingredients_url = UrlList.BASE_URL + UrlList.INGREDIENTS_URL
    buns = [ingredient["_id"] for ingredient in requests.get(ingredients_url).json()["data"] if ingredient["type"] == "bun"]
    ingredients = [ingredient["_id"] for ingredient in requests.get(ingredients_url).json()["data"] if ingredient["type"] != "bun"]

    payload = {
        "ingredients": [random.choice(buns), random.choice(ingredients)]
    }
    return payload