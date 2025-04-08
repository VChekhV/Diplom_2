from helpers.helpers import generate_user
from data import UrlList, AnswersList
import requests
import allure

class TestApiSignInPost:
    @allure.title("Логин пользователя с валидными данными")
    def test_sing_in_user(self):
        sign_up_url = UrlList.BASE_URL + UrlList.REGISTER_URL
        sign_in_url = UrlList.BASE_URL + UrlList.LOGIN_URL
        payload = generate_user()
        requests.post(sign_up_url, data=payload)
        del payload["name"]
        sign_in_response = requests.post(sign_in_url, data=payload)
        sign_in_response_dict_keys = list(sign_in_response.json().keys())
        print(sign_in_response.json())
        assert sign_in_response.status_code == 200
        assert sign_in_response_dict_keys == ['success', 'accessToken', 'refreshToken', 'user']

    @allure.title("Логин пользователя с неккоректной почтой")
    def test_sign_in_user_incorrect_email(self):
        sign_up_url = UrlList.BASE_URL + UrlList.REGISTER_URL
        sign_in_url = UrlList.BASE_URL + UrlList.LOGIN_URL
        payload = generate_user()
        requests.post(sign_up_url, data=payload)
        payload["email"] = "qwerty@qwerty.ru"
        del payload["name"]
        sign_in_response = requests.post(sign_in_url, data=payload)
        sign_in_response_dict = sign_in_response.json()
        assert sign_in_response.status_code == 401
        assert sign_in_response_dict == AnswersList.INCORRECT_DATA_ANSWER

    @allure.title("Логин пользователя с неккоректным паролем")
    def test_sign_in_user_incorrect_password(self):
        sign_up_url = UrlList.BASE_URL + UrlList.REGISTER_URL
        sign_in_url = UrlList.BASE_URL + UrlList.LOGIN_URL
        payload = generate_user()
        requests.post(sign_up_url, data=payload)
        payload["password"] = "qwerty"
        del payload["name"]
        sign_in_response = requests.post(sign_in_url, data=payload)
        sign_in_response_dict = sign_in_response.json()
        assert sign_in_response.status_code == 401
        assert sign_in_response_dict == AnswersList.INCORRECT_DATA_ANSWER