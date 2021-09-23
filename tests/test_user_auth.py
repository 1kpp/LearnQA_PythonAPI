import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
import requests


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
        url = 'https://playground.learnqa.ru/api/user/login'
        response_1 = requests.post(url, data=data)
        self.auth_sid = self.get_cookie(response_1, "auth_sid")
        self.token = self.get_header(response_1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response_1, "user_id")

    def test_auth_user(self):
        url = 'https://playground.learnqa.ru/api/user/auth'
        headers = {
            "x-csrf-token": self.token
        }
        cookies = {
            "auth_sid": self.auth_sid
        }
        response_2 = requests.get(url, headers=headers, cookies=cookies)
        Assertions.assert_json_value_by_name(
            response_2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method")

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):
        url = 'https://playground.learnqa.ru/api/user/auth'
        if condition == "no_cookie":
            headers = {
                "x-csrf-token": self.token
            }
            response = requests.get(url, headers=headers)
        else:
            cookies = {
                "auth_sid": self.auth_sid
            }
            response = requests.get(url, cookies=cookies)
        Assertions.assert_json_value_by_name(
            response,
            "user_id",
            0,
            f'User is authorized with condition - {condition}')
