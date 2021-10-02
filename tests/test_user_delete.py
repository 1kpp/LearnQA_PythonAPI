from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    def test_delete_user_with_id_2(self):
        loggin_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        logged_in_user = self.login_user(loggin_data)

        response = MyRequests.delete('/user/2',
                                     headers={'x-csrf-token': logged_in_user["token"]},
                                     cookies={"auth_sid": logged_in_user["auth_sid"]})
        Assertions.assert_response_text(response, 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')
        Assertions.assert_code_status(response, 400)

    def test_create_user_delete_it_and_try_to_get_him(self):
        # REGISTER
        registered_user = self.register_user()
        # LOGIN
        login_data = {
            'email': registered_user['email'],
            'password': registered_user['password']
        }
        logged_in_user = self.login_user(login_data)
        # DELETE
        response = MyRequests.delete(f'/user/{registered_user["user_id"]}',
                                     headers={'x-csrf-token': logged_in_user["token"]},
                                     cookies={"auth_sid": logged_in_user["auth_sid"]})
        # GET DELETED USER
        response_2 = MyRequests.get(f'/user/{registered_user["user_id"]}',
                                    headers={'x-csrf-token': logged_in_user["token"]},
                                    cookies={"auth_sid": logged_in_user["auth_sid"]})
        Assertions.assert_response_text(response_2, "User not found")
        Assertions.assert_code_status(response_2, 404)

    def test_try_to_delete_user_being_authorized_as_other_user(self):
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
        # DELETE 1ST USER WITH ID OF THE SECOND USER
        new_name = 'changed_name'
        response_2 = MyRequests.delete(f'/user/{second_registered_user["user_id"]}',
                                       headers={'x-csrf-token': logged_in_first_user["token"]},
                                       cookies={"auth_sid": logged_in_first_user["auth_sid"]})
        Assertions.assert_code_status(response_2, 404)
