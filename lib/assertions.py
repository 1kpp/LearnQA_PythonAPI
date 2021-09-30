from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json format, response text is {response.text}'
        assert name in response_as_dict, f'Response json doesnt have key name "{name}"'
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json format, response text is {response.text}'
        assert name in response_as_dict, f'Response json doesnt have key name "{name}"'

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json format, response text is {response.text}'
        for name in names:
            assert name in response_as_dict, f'Response json doesnt have key name "{name}"'

    @staticmethod
    def assert_code_status(response: Response, code):
        assert response.status_code == code, f'Unexpected status code. Expected: {code}, actual: {response.status_code}'

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json format, response text is {response.text}'
        assert name not in response_as_dict, f'Response json has key name "{name}"'
