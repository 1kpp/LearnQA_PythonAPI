import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


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

    def test_auth_user(self):
        headers = {
            "x-csrf-token": self.token
        }
        cookies = {
            "auth_sid": self.auth_sid
        }
        response_2 = MyRequests.get('/user/auth', headers=headers, cookies=cookies)
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
            response = MyRequests.get('/user/auth', headers=headers)
        else:
            cookies = {
                "auth_sid": self.auth_sid
            }
            response = MyRequests.get('/user/auth', cookies=cookies)
        Assertions.assert_json_value_by_name(
            response,
            "user_id",
            0,
            f'User is authorized with condition - {condition}')
