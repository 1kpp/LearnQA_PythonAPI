from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get('/user/2')
        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.post('/user/login', data=data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response, 'user_id')

        response_2 = MyRequests.get(f'/user/{user_id_from_auth_method}', headers={'x-csrf-token': token},
                                    cookies={"auth_sid": auth_sid})
        expected_fields = ['username', 'email', 'firstName', 'lastName']
        Assertions.assert_json_has_keys(response_2, expected_fields)

    def test_get_user_details_auth_as_other_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.post('/user/login', data=data)
        data = self.prepare_registration_data()
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, 'x-csrf-token')
        response_2 = MyRequests.post("/user/", data=data)
        id_of_another_user = self.get_json_value(response_2, "id")
        response_3 = MyRequests.get(f'/user/{id_of_another_user}', headers={'x-csrf-token': token},
                                    cookies={"auth_sid": auth_sid})
        Assertions.assert_json_has_key(response_3, 'username')
        Assertions.assert_json_has_not_key(response_3, 'email')
        Assertions.assert_json_has_not_key(response_3, 'firstName')
        Assertions.assert_json_has_not_key(response_3, 'lastName')
