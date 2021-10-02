import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_json_has_key(response, "id")
        Assertions.assert_code_status(response, 200), f"Unexpected status code: {response.status_code}"

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            f"Unexpected response content: {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email=email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format",\
            f"Unexpected response content: {response.content}"

    required_fileds = [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ]

    @pytest.mark.parametrize("data", required_fileds)
    def test_create_user_without_one_required_field(self, data):
        payload = self.prepare_registration_data_without_one_field(data)
        response = MyRequests.post("/user/", data=payload)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, f'The following required params are missed: {data}')

    def test_create_user_with_shortname(self):
        username = self.random_string(1)
        data = self.prepare_registration_data(username=username)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, "The value of 'username' field is too short")

    def test_create_user_with_too_long_name(self):
        username = self.random_string(255)
        data = self.prepare_registration_data(username=username)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, "The value of 'username' field is too long")