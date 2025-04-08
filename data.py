class UrlList:
    BASE_URL = "https://stellarburgers.nomoreparties.site"
    INGREDIENTS_URL = "/api/ingredients"
    ORDER_URL = "/api/orders"
    RESET_PASSWORD_URL = "/api/password-reset"
    REGISTER_URL = "/api/auth/register"
    LOGIN_URL = "/api/auth/login"
    LOGOUT_URL = "/api/auth/logout "
    PERSON_INFO_URL = "/api/auth/user"

class AnswersList:
    SAME_USER_ANSWER = {
        "success": False,
        "message": "User already exists",
    }
    EMPTY_FIELD_ANSWER = {
        "success": False,
        "message": "Email, password and name are required fields",
    }
    INCORRECT_DATA_ANSWER = {
        "success": False,
        "message": "email or password are incorrect",
    }
    NOT_AUTHORISED_ANSWER = {
        "success": False,
        "message": "You should be authorised",
    }
    CHANGE_SAME_EMAIL_ANSWER = {
        "success": False,
        "message": "User with such email already exists",
    }
    CHANGE_INFO_NOT_AUTHORISED_ANSWER = {
        "success": False,
        "message": "You should be authorised",
    }
    ORDER_WITHOUT_INGREDIENTS = {
        "success": False,
        "message": "Ingredient ids must be provided",
    }
    SERVER_ERROR = "Internal Server Error"