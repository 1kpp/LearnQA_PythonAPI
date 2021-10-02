import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic('Getting user info cases')
class TestUserGet(BaseCase):
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_not_auth(self):
        with allure.step('Try to get user info being not authorized'):
            response = MyRequests.get('/user/2')
        with allure.step('Result check'):
            Assertions.assert_json_has_key(response, 'username')
            Assertions.assert_json_has_not_key(response, 'email')
            Assertions.assert_json_has_not_key(response, 'firstName')
            Assertions.assert_json_has_not_key(response, 'lastName')

    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_auth_as_same_user(self):
        with allure.step('Get login data'):
            login_data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
        with allure.step('Login'):
            logged_in_user = self.login_user(login_data)
        with allure.step('Get info of a logged in user'):
            response_2 = MyRequests.get(f'/user/{logged_in_user["user_id"]}',
                                        headers={'x-csrf-token': logged_in_user["token"]},
                                        cookies={"auth_sid": logged_in_user["auth_sid"]})
        with allure.step('Result check'):
            expected_fields = ['username', 'email', 'firstName', 'lastName']
            Assertions.assert_json_has_keys(response_2, expected_fields)

    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_auth_as_other_user(self):
        with allure.step('Get login data of a first user'):
            login_data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
        with allure.step('Login as a first user'):
            logged_in_first_user = self.login_user(login_data)
        with allure.step('Login as a first user'):
            logged_in_second_user = self.register_user()
        with allure.step('Get user info of second user being authorized as first'):
            response_3 = MyRequests.get(f'/user/{logged_in_second_user["user_id"]}',
                                        headers={'x-csrf-token': logged_in_first_user["token"]},
                                        cookies={"auth_sid": logged_in_first_user["auth_sid"]})
        with allure.step('Result check'):
            Assertions.assert_json_has_key(response_3, 'username')
            Assertions.assert_json_has_not_key(response_3, 'email')
            Assertions.assert_json_has_not_key(response_3, 'firstName')
            Assertions.assert_json_has_not_key(response_3, 'lastName')
