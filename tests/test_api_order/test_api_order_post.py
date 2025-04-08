from helpers.helpers import generate_user, generate_order
from data import UrlList, AnswersList
import requests
import allure

class TestApiOrderPost:

    @allure.title("Создание заказа без авторизации с валидными данными")
    def test_create_order_not_authorised(self):
        url = UrlList.BASE_URL + UrlList.ORDER_URL
        payload = generate_order()
        order_response = requests.post(url, data=payload)
        order_response_dict_keys = list(order_response.json().keys())
        assert order_response.status_code == 200
        assert order_response_dict_keys == ["success", "name", "order"]

    @allure.title("Создание заказа без авторизации без ингредиентов")
    def test_create_order_not_authorised_without_ingredients(self):
        url = UrlList.BASE_URL + UrlList.ORDER_URL
        payload = {
            "ingredients": [],
        }
        order_response = requests.post(url, data=payload)
        order_response_dict = order_response.json()
        assert order_response.status_code == 400
        assert order_response_dict == AnswersList.ORDER_WITHOUT_INGREDIENTS

    @allure.title("Создание заказа с неправильными ингредиентами, пользователь неавторизирован")
    def test_create_order_not_authorised_wrong_ingredients(self):
        url = UrlList.BASE_URL + UrlList.ORDER_URL
        payload = {
            "ingredients": ["60d3b41abdacab0026a733c6","600006e4dc000e00000b000"],
        }
        order_response = requests.post(url, data=payload)
        order_response_text = order_response.text
        assert order_response.status_code == 500
        assert AnswersList.SERVER_ERROR in order_response_text

    @allure.title("Создание заказа с авторизацией с валидными данными")
    def test_create_order_authorised(self):
        url = UrlList.BASE_URL + UrlList.ORDER_URL
        sign_up_url = UrlList.BASE_URL + UrlList.REGISTER_URL
        sign_in_url = UrlList.BASE_URL + UrlList.LOGIN_URL
        payload = generate_user()
        requests.post(sign_up_url, data=payload)
        del payload["name"]
        requests.post(sign_in_url, data=payload)
        payload = generate_order()
        order_response = requests.post(url, data=payload)
        order_response_dict_keys = list(order_response.json().keys())
        assert order_response.status_code == 200
        assert order_response_dict_keys == ["success", "name", "order"]

    @allure.title("Создание заказа с авторизацией без ингредиентов")
    def test_create_order_authorised_without_ingredients(self):
        url = UrlList.BASE_URL + UrlList.ORDER_URL
        sign_up_url = UrlList.BASE_URL + UrlList.REGISTER_URL
        sign_in_url = UrlList.BASE_URL + UrlList.LOGIN_URL
        payload = generate_user()
        requests.post(sign_up_url, data=payload)
        del payload["name"]
        requests.post(sign_in_url, data=payload)
        payload = {
            "ingredients": [],
        }
        order_response = requests.post(url, data=payload)
        order_response_dict = order_response.json()
        assert order_response.status_code == 400
        assert order_response_dict == AnswersList.ORDER_WITHOUT_INGREDIENTS

    @allure.title("Создание заказа с неправильными ингредиентами, пользователь авторизирован")
    def test_create_order_authorised_wrong_ingredients(self):
        url = UrlList.BASE_URL + UrlList.ORDER_URL
        sign_up_url = UrlList.BASE_URL + UrlList.REGISTER_URL
        sign_in_url = UrlList.BASE_URL + UrlList.LOGIN_URL
        payload = generate_user()
        requests.post(sign_up_url, data=payload)
        del payload["name"]
        requests.post(sign_in_url, data=payload)
        payload = {
            "ingredients": ["60d3b41abdacab0026a733c6","600006e4dc000e00000b000"],
        }
        order_response = requests.post(url, data=payload)
        order_response_text = order_response.text
        assert order_response.status_code == 500
        assert AnswersList.SERVER_ERROR in order_response_text