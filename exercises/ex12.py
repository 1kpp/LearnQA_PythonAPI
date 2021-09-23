import requests


class TestHeader:
    def test_get_header(self):
        url = 'https://playground.learnqa.ru/api/homework_header'
        res = requests.get(url)
        assert "x-secret-homework-header" in res.headers, f'No header named "x-secret-homework-header"'
        actual_header = res.headers.get('x-secret-homework-header')
        expected_header = 'Some secret value'
        assert actual_header == expected_header, f'Actual header is not equal to expected one. Actual - {actual_header}'
