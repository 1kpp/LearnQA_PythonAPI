import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic('Deletion cases')
class TestUserDelete(BaseCase):
    @allure.severity(allure.severity_level.MINOR)
    def test_delete_user_with_id_2(self):
        with allure.step('Get login data'):
            loggin_data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
        with allure.step('Login'):
            logged_in_user = self.login_user(loggin_data)
        with allure.step('Try to delete user with id=2'):
            response = MyRequests.delete('/user/2',
                                         headers={'x-csrf-token': logged_in_user["token"]},
                                         cookies={"auth_sid": logged_in_user["auth_sid"]})
        with allure.step('Result check'):
            Assertions.assert_response_text(response, 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')
            Assertions.assert_code_status(response, 400)

    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_delete_it_and_try_to_get_him(self):
        with allure.step('Register user'):
            registered_user = self.register_user()
        with allure.step('Get login data of registered user'):
            login_data = {
                'email': registered_user['email'],
                'password': registered_user['password']
            }
        with allure.step('Login'):
            logged_in_user = self.login_user(login_data)
        with allure.step('Delete created user'):
            response = MyRequests.delete(f'/user/{registered_user["user_id"]}',
                                         headers={'x-csrf-token': logged_in_user["token"]},
                                         cookies={"auth_sid": logged_in_user["auth_sid"]})
        with allure.step('Try to get info of deleted user'):
            response_2 = MyRequests.get(f'/user/{registered_user["user_id"]}',
                                        headers={'x-csrf-token': logged_in_user["token"]},
                                        cookies={"auth_sid": logged_in_user["auth_sid"]})
        with allure.step('Result check'):
            Assertions.assert_response_text(response_2, "User not found")
            Assertions.assert_code_status(response_2, 404)

    @allure.severity(allure.severity_level.CRITICAL)
    def test_try_to_delete_user_being_authorized_as_other_user(self):
        with allure.step('Register first user'):
            first_registered_user = self.register_user()
        with allure.step('Register second user'):
            second_registered_user = self.register_user()
        with allure.step('Get login data of the first user'):
            login_data = {
                'email': first_registered_user['email'],
                'password': first_registered_user['password']
            }
        with allure.step('Login as a first user'):
            logged_in_first_user = self.login_user(login_data)
        with allure.step('Try to delete second user with headers and cookie of the first one'):
            response_2 = MyRequests.delete(f'/user/{second_registered_user["user_id"]}',
                                           headers={'x-csrf-token': logged_in_first_user["token"]},
                                           cookies={"auth_sid": logged_in_first_user["auth_sid"]})
        with allure.step('Result check'):
            Assertions.assert_code_status(response_2, 404)
