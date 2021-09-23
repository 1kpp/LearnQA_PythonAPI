import json
from requests import Response


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Can't find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Can't find cookie with name {header_name} in the last response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
            print(response_as_dict)
        except json.decoder.JSONDecodeError:
            assert False, f'Response is not in json format, response is {response.text}'
        assert name in response_as_dict, f'Response doesnt have key "{name}". {response.json()}'
        return response_as_dict[name]
