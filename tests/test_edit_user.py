from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestEditUser(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        registered_user = self.register_user()
        # LOGIN
        login_data = {
            'email': registered_user['email'],
            'password': registered_user['password']
        }
        logged_in_user = self.login_user(login_data)
        # EDIT
        new_name = 'changed_name'
        response_3 = MyRequests.put(f'/user/{registered_user["user_id"]}',
                                    headers={'x-csrf-token': logged_in_user["token"]},
                                    cookies={"auth_sid": logged_in_user["auth_sid"]},
                                    data={'firstName': new_name})
        Assertions.assert_code_status(response_3, 200)
        # GET
        response_4 = MyRequests.get(f'/user/{registered_user["user_id"]}',
                                    headers={'x-csrf-token': logged_in_user["token"]},
                                    cookies={"auth_sid": logged_in_user["auth_sid"]})
        Assertions.assert_json_value_by_name(response_4, 'firstName', new_name, 'Wrong name after edition')

    def test_edit_user_being_unauthorized(self):
        new_name = 'changed_name'
        response_2 = MyRequests.put('/user/2', data={'firstName': new_name})
        Assertions.assert_response_text(response_2, 'Auth token not supplied')
        Assertions.assert_code_status(response_2, 400)

    def test_edit_user_being_authorized_as_other_user(self):
        # REGISTER 1ST USER
        first_registered_user = self.register_user()
        # REGISTER 2ND USER
        second_registered_user = self.register_user()
        # LOGIN AS 1ST USER
        login_data = {
            'email': first_registered_user['email'],
            'password': first_registered_user['password']
        }
        logged_in_first_user = self.login_user(login_data)

        # EDIT 1ST USER WITH ID OF THE SECOND USER
        new_name = 'changed_name'
        response_4 = MyRequests.put(f'/user/{second_registered_user["user_id"]}',
                                    headers={'x-csrf-token': logged_in_first_user["token"]},
                                    cookies={"auth_sid": logged_in_first_user["auth_sid"]},
                                    data={'firstName': new_name})
        # GET
        response_5 = MyRequests.get(f'/user/{first_registered_user["user_id"]}',
                                    headers={'x-csrf-token': logged_in_first_user["token"]},
                                    cookies={"auth_sid": logged_in_first_user["auth_sid"]})
        Assertions.assert_json_value_by_name(response_5,
                                             'firstName', first_registered_user['firstName'],
                                             f'The name "{first_registered_user["firstName"]}" shouldnt be changed to "{new_name}"!')
        Assertions.assert_code_status(response_4, 400)

    def test_change_user_email(self):
        # REGISTER
        registered_user = self.register_user()
        # LOGIN
        login_data = {
            'email': registered_user['email'],
            'password': registered_user['password']
        }
        # LOGIN
        login_data = {
            'email': registered_user['email'],
            'password': registered_user['password']
        }
        logged_in_user = self.login_user(login_data)
        # EDIT
        email_to_change = 'emailexample.com'
        response_3 = MyRequests.put(f'/user/{registered_user["user_id"]}',
                                    headers={'x-csrf-token': logged_in_user["token"]},
                                    cookies={"auth_sid": logged_in_user["auth_sid"]},
                                    data={'email': email_to_change})
        Assertions.assert_response_text(response_3, "Invalid email format")
        Assertions.assert_code_status(response_3, 400)

    def test_change_username_on_a_short_one(self):
        # REGISTER
        registered_user = self.register_user()
        # LOGIN
        login_data = {
            'email': registered_user['email'],
            'password': registered_user['password']
        }
        # LOGIN
        login_data = {
            'email': registered_user['email'],
            'password': registered_user['password']
        }
        logged_in_user = self.login_user(login_data)
        # EDIT
        new_name = self.random_string(1)
        response_3 = MyRequests.put(f'/user/{registered_user["user_id"]}',
                                    headers={'x-csrf-token': logged_in_user["token"]},
                                    cookies={"auth_sid": logged_in_user["auth_sid"]},
                                    data={'firstName': new_name})
        Assertions.assert_json_value_by_name(response_3, 'error',
                                             "Too short value for field firstName",
                                             f"Users cant have short names like {new_name}")
        Assertions.assert_code_status(response_3, 400)

