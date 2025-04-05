from helpers.helpers import generate_user
from data import UrlList, AnswersList
import requests
import allure


class TestApiSignUpPost:
    @allure.title("Регистрация пользователя с валидными данными")
    def test_create_user(self):
        url = UrlList.BASE_URL + UrlList.REGISTER_URL
        payload = generate_user()
        response = requests.post(url, data=payload)
        response_dict_keys = list(response.json().keys())
        assert response.status_code == 200
        assert response_dict_keys == ['success', 'user', 'accessToken', 'refreshToken']

    @allure.title("Регистрация пользователя, который уже зарегистрирован")
    def test_same_user_not_registred(self):
        url = UrlList.BASE_URL + UrlList.REGISTER_URL
        payload = generate_user()
        requests.post(url, data=payload)
        response_2 = requests.post(url, data=payload)
        response_2_dict = response_2.json()
        assert response_2.status_code == 403
        assert response_2_dict == AnswersList.SAME_USER_ANSWER

    @allure.title("Регистрация пользователя без указания пароля")
    def test_create_user_without_password(self):
        url = UrlList.BASE_URL + UrlList.REGISTER_URL
        payload = generate_user()
        payload["password"] = ""
        response = requests.post(url, data=payload)
        response_dict = response.json()
        assert response.status_code == 403
        assert response_dict == AnswersList.EMPTY_FIELD_ANSWER

    @allure.title("Регистрация пользователя без указания почты")
    def test_create_user_without_email(self):
        url = UrlList.BASE_URL + UrlList.REGISTER_URL
        payload = generate_user()
        payload["email"] = ""
        response = requests.post(url, data=payload)
        response_dict = response.json()
        assert response.status_code == 403
        assert response_dict == AnswersList.EMPTY_FIELD_ANSWER

    @allure.title("Регистрация пользователя без указания имени")
    def test_create_user_without_name(self):
        url = UrlList.BASE_URL + UrlList.REGISTER_URL
        payload = generate_user()
        payload["name"] = ""
        response = requests.post(url, data=payload)
        response_dict = response.json()
        assert response.status_code == 403
        assert response_dict == AnswersList.EMPTY_FIELD_ANSWER