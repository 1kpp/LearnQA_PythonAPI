import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic('Authorization cases')
class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookie",
        "no_header"
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_1 = MyRequests.post('/user/login', data=data)
        self.auth_sid = self.get_cookie(response_1, "auth_sid")
        self.token = self.get_header(response_1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response_1, "user_id")

    @allure.severity(allure.severity_level.CRITICAL)
    def test_auth_user(self):
        with allure.step('Get auth data'):
            headers = {
                "x-csrf-token": self.token
            }
            cookies = {
                "auth_sid": self.auth_sid
            }
        with allure.step('Auth user'):
            response_2 = MyRequests.get('/user/auth', headers=headers, cookies=cookies)
        with allure.step('Result check'):
            Assertions.assert_json_value_by_name(
                response_2,
                "user_id",
                self.user_id_from_auth_method,
                "User id from auth method is not equal to user id from check method")

    @pytest.mark.parametrize("condition", exclude_params)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            with allure.step('Get header'):
                headers = {
                    "x-csrf-token": self.token
                }
            with allure.step('Try auth with no cookie'):
                response = MyRequests.get('/user/auth', headers=headers)
        else:
            with allure.step('Get cookie'):
                cookies = {
                    "auth_sid": self.auth_sid
                }
            with allure.step('Try auth with no header'):
                response = MyRequests.get('/user/auth', cookies=cookies)
        with allure.step('Result check'):
            Assertions.assert_json_value_by_name(
                response,
                "user_id",
                0,
                f'User is authorized with condition - {condition}')
