from helpers.helpers import generate_user
from data import UrlList, AnswersList
import requests
import allure
from faker import Faker


class TestApiChangeInfoPatch:

    @allure.title("Изменение данных у авторизированного пользователя")
    def test_change_user_info(self):
        fake = Faker(["ru_RU"])
        profile_url = UrlList.BASE_URL + UrlList.PERSON_INFO_URL
        sign_up_url = UrlList.BASE_URL + UrlList.REGISTER_URL
        sign_in_url = UrlList.BASE_URL + UrlList.LOGIN_URL

        with allure.step("1. Регистрация нового пользователя"):
            payload = generate_user()
            requests.post(sign_up_url, data=payload)

        with allure.step("2. Авторизация пользователя"):
            sign_in_response = requests.post(sign_in_url, data=payload)
            token = sign_in_response.json()["accessToken"]
            headers = {"authorization": token}

        with allure.step("3. Подготовка новых данных для обновления"):
            update_profile = {
                "email": fake.ascii_email(),
                "name": fake.first_name(),
            }

        with allure.step("4. Отправка PATCH-запроса для обновления данных"):
            patch_response = requests.patch(profile_url, headers=headers, data=update_profile)

        with allure.step("5. Проверка ответа"):
            assert patch_response.status_code == 200
            assert patch_response.json() == {
                "success": True,
                "user": update_profile,
            }

    @allure.title("Изменение данных у авторизированного пользователя, email повторяется")
    def test_change_user_info_same_email(self):
        fake = Faker(["ru_RU"])
        profile_url = UrlList.BASE_URL + UrlList.PERSON_INFO_URL
        sign_up_url = UrlList.BASE_URL + UrlList.REGISTER_URL
        sign_in_url = UrlList.BASE_URL + UrlList.LOGIN_URL

        with allure.step("1. Регистрация первого пользователя"):
            payload_1 = generate_user()
            requests.post(sign_up_url, data=payload_1)

        with allure.step("2. Регистрация второго пользователя"):
            payload_2 = generate_user()
            sign_up_response_2 = requests.post(sign_up_url, data=payload_2)
            sign_in_response_2_dict = sign_up_response_2.json()["user"]

        with allure.step("3. Авторизация первого пользователя"):
            sign_in_response = requests.post(sign_in_url, data=payload_1)
            token = sign_in_response.json()["accessToken"]
            headers = {"authorization": token}

        with allure.step("4. Попытка изменить email на уже существующий"):
            update_profile = {
                "email": sign_in_response_2_dict["email"],
                "name": fake.first_name(),
            }
            patch_response = requests.patch(profile_url, headers=headers, data=update_profile)

        with allure.step("5. Проверка ошибки"):
            assert patch_response.status_code == 403
            assert patch_response.json() == AnswersList.CHANGE_SAME_EMAIL_ANSWER

    @allure.title("Изменение данных у неавторизированного пользователя")
    def test_change_user_info_not_authorised(self):
        fake = Faker(["ru_RU"])
        profile_url = UrlList.BASE_URL + UrlList.PERSON_INFO_URL
        sign_up_url = UrlList.BASE_URL + UrlList.REGISTER_URL

        with allure.step("1. Регистрация пользователя"):
            payload = generate_user()
            requests.post(sign_up_url, data=payload)

        with allure.step("2. Попытка изменить данные без авторизации"):
            token = ""
            headers = {"authorization": token}
            update_profile = {
                "email": fake.ascii_email(),
                "name": fake.first_name(),
            }
            patch_response = requests.patch(profile_url, headers=headers, data=update_profile)

        with allure.step("3. Проверка ошибки доступа"):
            assert patch_response.status_code == 401
            assert patch_response.json() == AnswersList.CHANGE_INFO_NOT_AUTHORISED_ANSWER