import json
import random
import string
from lib.my_requests import MyRequests
from lib.assertions import Assertions
from datetime import datetime
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

    def prepare_registration_data(self, email=None, password=None, username=None, firstName=None, lastName=None):
        if email is None:
            base_part = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime("%h%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': self.random_string() if password is None else password,
            'username': self.random_string() if username is None else username,
            'firstName': self.random_string() if firstName is None else firstName,
            'lastName': self.random_string() if lastName is None else lastName,
            'email': email,
        }

    def register_user(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.post('/user/', data=register_data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')
        result = {}

        result.update({'email': register_data['email']})
        result.update({'firstName': register_data['firstName']})
        result.update({'password': register_data['password']})
        result.update({'user_id': self.get_json_value(response, 'id')})
        return result

    def login_user(self, login_data):
        response_2 = MyRequests.post('/user/login', data=login_data)
        result = {}
        result.update({'auth_sid': self.get_cookie(response_2, "auth_sid")})
        result.update({'token': self.get_header(response_2, 'x-csrf-token')})
        return result

    def prepare_registration_data_without_one_field(self, field):
        if field == 'password':
            data = {
                'username': self.random_string(),
                'firstName': self.random_string(),
                'lastName': self.random_string(),
                'email': f'{self.random_string()}@example.com',
            }
        elif field == 'username':
            data = {
                'password': self.random_string(),
                'firstName': self.random_string(),
                'lastName': self.random_string(),
                'email': f'{self.random_string()}@example.com',
            }
        elif field == 'firstName':
            data = {
                'password': self.random_string(),
                'username': self.random_string(),
                'lastName': self.random_string(),
                'email': f'{self.random_string()}@example.com',
            }
        elif field == 'lastName':
            data = {
                'password': self.random_string(),
                'username': self.random_string(),
                'firstName': self.random_string(),
                'email': f'{self.random_string()}@example.com',
            }
        else:
            data = {
                'password': self.random_string(),
                'username': self.random_string(),
                'firstName': self.random_string(),
                'lastName': self.random_string()
            }
        return data

    def random_string(self, length: int = None):
        if length is None:
            maxlen = random.randrange(8, 10)
        else:
            maxlen = length
        symbols = string.ascii_letters + string.digits
        x = "".join([random.choice(symbols) for i in range(maxlen)])
        return x
