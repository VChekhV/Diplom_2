from helpers.helpers import generate_user, generate_order
from data import UrlList, AnswersList
import requests
import allure


class TestApiOrderPost:

    @allure.title("Получение заказов неавторизированного пользователя")
    def test_get_orders_list_not_authorised(self):
        url = UrlList.BASE_URL + UrlList.ORDER_URL
        sign_up_url = UrlList.BASE_URL + UrlList.REGISTER_URL
        sign_in_url = UrlList.BASE_URL + UrlList.LOGIN_URL
        logout_url = UrlList.BASE_URL + UrlList.LOGOUT_URL
        payload = generate_user()
        requests.post(sign_up_url, data=payload)
        del payload["name"]
        sign_in_response = requests.post(sign_in_url, data=payload)
        sign_in_response_dict = sign_in_response.json()
        refresh_token = sign_in_response_dict["refreshToken"]
        payload = generate_order()
        token = {
            "token": refresh_token,
        }
        requests.post(url, data=payload)
        requests.post(logout_url, data=token)
        orders_list_response = requests.get(url)
        orders_list_response_dict = orders_list_response.json()
        assert orders_list_response.status_code == 401
        assert orders_list_response_dict == AnswersList.NOT_AUTHORISED_ANSWER

    @allure.title("Получение заказов авторизированного пользователя")
    def test_get_orders_list_authorised(self):
        url = UrlList.BASE_URL + UrlList.ORDER_URL
        sign_up_url = UrlList.BASE_URL + UrlList.REGISTER_URL
        sign_in_url = UrlList.BASE_URL + UrlList.LOGIN_URL
        payload = generate_user()
        requests.post(sign_up_url, data=payload)
        del payload["name"]
        sign_in_response = requests.post(sign_in_url, data=payload)
        sign_in_response_dict = sign_in_response.json()
        access_token = sign_in_response_dict["accessToken"]
        payload = generate_order()
        headers = {
            "authorization": access_token,
        }
        requests.post(url, data=payload)
        orders_list_response = requests.get(url, headers=headers)
        orders_list_response_dict_keys = list(orders_list_response.json().keys())
        assert orders_list_response.status_code == 200
        assert orders_list_response_dict_keys == ["success", "orders", "total", "totalToday"]