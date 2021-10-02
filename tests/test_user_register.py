import pytest
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic('Registration cases')
class TestUserRegister(BaseCase):
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_successfully(self):
        with allure.step('Get registration data'):
            data = self.prepare_registration_data()
        with allure.step('Create user'):
            response = MyRequests.post("/user/", data=data)
        with allure.step('Result check'):
            Assertions.assert_json_has_key(response, "id")
            Assertions.assert_code_status(response, 200), f"Unexpected status code: {response.status_code}"

    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_existing_email(self):
        with allure.step('Get registration data with email of existing user'):
            email = 'vinkotov@example.com'
            data = self.prepare_registration_data(email)
        with allure.step('Create user'):
            response = MyRequests.post("/user/", data=data)
        with allure.step('Result check'):
            Assertions.assert_response_text(response, f"Users with email '{email}' already exists")

    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_incorrect_email(self):
        with allure.step('Get registration data with incorrect email'):
            email = 'vinkotovexample.com'
            data = self.prepare_registration_data(email=email)
        with allure.step('Create user'):
            response = MyRequests.post("/user/", data=data)
        with allure.step('Result check'):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_response_text(response, "Invalid email format")

    required_fileds = [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ]

    @pytest.mark.parametrize("data", required_fileds)
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_without_one_required_field(self, data):
        with allure.step('Get registration data'):
            payload = self.prepare_registration_data_without_one_field(data)
        with allure.step('Create user'):
            response = MyRequests.post("/user/", data=payload)
        with allure.step('Result check'):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_response_text(response, f'The following required params are missed: {data}')

    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_shortname(self):
        with allure.step('Get registration data'):
            username = self.random_string(1)
            data = self.prepare_registration_data(username=username)
        with allure.step('Create user'):
            response = MyRequests.post("/user/", data=data)
        with allure.step('Result check'):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_response_text(response, "The value of 'username' field is too short")

    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_too_long_name(self):
        with allure.step('Get registration data'):
            username = self.random_string(255)
            data = self.prepare_registration_data(username=username)
        with allure.step('Create user'):
            response = MyRequests.post("/user/", data=data)
        with allure.step('Result check'):
            Assertions.assert_code_status(response, 400)
            Assertions.assert_response_text(response, "The value of 'username' field is too long")
