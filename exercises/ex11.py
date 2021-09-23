import requests


class TestCookie:
    def test_get_cookie(self):
        url = 'https://playground.learnqa.ru/api/homework_cookie'
        res = requests.get(url)
        assert "HomeWork" in res.cookies, f'No cookie named HomeWork'
        assert res.cookies.get('HomeWork') == 'hw_value', f'Cookie has another value - {res.cookies["HomeWork"]}'
