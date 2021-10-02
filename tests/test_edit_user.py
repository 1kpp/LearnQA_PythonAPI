import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic('Edition cases')
class TestEditUser(BaseCase):
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_just_created_user(self):
        with allure.step('Register user'):
            registered_user = self.register_user()
        with allure.step('Get login data of a registered user'):
            login_data = {
                'email': registered_user['email'],
                'password': registered_user['password']
            }
        with allure.step('Login'):
            logged_in_user = self.login_user(login_data)
        with allure.step('Edit user'):
            new_name = 'changed_name'
            response_3 = MyRequests.put(f'/user/{registered_user["user_id"]}',
                                        headers={'x-csrf-token': logged_in_user["token"]},
                                        cookies={"auth_sid": logged_in_user["auth_sid"]},
                                        data={'firstName': new_name})
        with allure.step('Get info of eddited user'):
            response_4 = MyRequests.get(f'/user/{registered_user["user_id"]}',
                                        headers={'x-csrf-token': logged_in_user["token"]},
                                        cookies={"auth_sid": logged_in_user["auth_sid"]})
        with allure.step('Result check'):
            Assertions.assert_json_value_by_name(response_4, 'firstName', new_name, 'Wrong name after edition')

    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_user_being_unauthorized(self):
        with allure.step('Get data to be changed'):
            new_name = 'changed_name'
        with allure.step('Try to change user data being not authorized'):
            response_2 = MyRequests.put('/user/2', data={'firstName': new_name})
        with allure.step('Result check'):
            Assertions.assert_response_text(response_2, 'Auth token not supplied')
            Assertions.assert_code_status(response_2, 400)

    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_user_being_authorized_as_other_user(self):
        with allure.step('Register first user'):
            first_registered_user = self.register_user()
        with allure.step('Register second user'):
            second_registered_user = self.register_user()
        with allure.step('Get login data of a first user'):
            login_data = {
                'email': first_registered_user['email'],
                'password': first_registered_user['password']
            }
        with allure.step('Login as a first user'):
            logged_in_first_user = self.login_user(login_data)
        with allure.step('Get data to be changed'):
            new_name = 'changed_name'
        with allure.step('Edit first user with id of the second user'):
            response_4 = MyRequests.put(f'/user/{second_registered_user["user_id"]}',
                                        headers={'x-csrf-token': logged_in_first_user["token"]},
                                        cookies={"auth_sid": logged_in_first_user["auth_sid"]},
                                        data={'firstName': new_name})
        with allure.step('Get info of a first user'):
            response_5 = MyRequests.get(f'/user/{first_registered_user["user_id"]}',
                                        headers={'x-csrf-token': logged_in_first_user["token"]},
                                        cookies={"auth_sid": logged_in_first_user["auth_sid"]})
        with allure.step('Result check'):
            Assertions.assert_json_value_by_name(response_5,
                                                 'firstName', first_registered_user['firstName'],
                                                 f'The name "{first_registered_user["firstName"]}" shouldnt be changed to "{new_name}"!')
            Assertions.assert_code_status(response_4, 400)

    @allure.severity(allure.severity_level.CRITICAL)
    def test_change_user_email(self):
        with allure.step('Register first user'):
            registered_user = self.register_user()
        with allure.step('Get login data of a registered user'):
            login_data = {
                'email': registered_user['email'],
                'password': registered_user['password']
            }
        with allure.step('Login'):
            logged_in_user = self.login_user(login_data)
        with allure.step('Get data to be changed'):
            email_to_change = 'emailexample.com'
        with allure.step('Change user email'):
            response_3 = MyRequests.put(f'/user/{registered_user["user_id"]}',
                                        headers={'x-csrf-token': logged_in_user["token"]},
                                        cookies={"auth_sid": logged_in_user["auth_sid"]},
                                        data={'email': email_to_change})
        with allure.step('Result check'):
            Assertions.assert_response_text(response_3, "Invalid email format")
            Assertions.assert_code_status(response_3, 400)

    @allure.severity(allure.severity_level.MINOR)
    def test_change_username_on_a_short_one(self):
        with allure.step('Register first user'):
            registered_user = self.register_user()
        with allure.step('Get login data of a registered user'):
            login_data = {
                'email': registered_user['email'],
                'password': registered_user['password']
            }
        with allure.step('Login'):
            logged_in_user = self.login_user(login_data)
        with allure.step('Get data to be changed'):
            new_name = self.random_string(1)
        with allure.step('Try to change firstName'):
            response_3 = MyRequests.put(f'/user/{registered_user["user_id"]}',
                                        headers={'x-csrf-token': logged_in_user["token"]},
                                        cookies={"auth_sid": logged_in_user["auth_sid"]},
                                        data={'firstName': new_name})
        with allure.step('Result check'):
            Assertions.assert_json_value_by_name(response_3, 'error',
                                                 "Too short value for field firstName",
                                                 f"Users cant have short names like {new_name}")
            Assertions.assert_code_status(response_3, 400)
