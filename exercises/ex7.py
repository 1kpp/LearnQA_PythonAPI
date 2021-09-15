import requests

url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'

# Part 1
response_1 = requests.get(url)
print(f'В случае http-запроса любого типа без параметра method выводится: "{response_1.text}"')
print('---------------------------------------------------------------------------------------')

# Part 2
data = {
    "method": "PATCH"
}
response_2 = requests.patch(url, data=data)
print(f'В случае запроса не из списка выводится: "{response_2.text}"')
print('---------------------------------------------------------------------------------------')

# Part 3
data = {
    "method": "DELETE"
}
response_3 = requests.delete(url, data=data)
print(f'В случае правильного значения method выводится : "{response_3.text}"')
print('---------------------------------------------------------------------------------------')

# Part 4
http_methods = ['post', 'get', 'put', 'delete']
method_values = ['POST', 'GET', 'PUT', 'DELETE']

for method in http_methods:
    if method == 'get':
        print('Перебор с методом "get":')
        print('---------------------------------------------------------------------------------------')
        for method_value in method_values:
            params = {
                "method": method_value
            }
            response = requests.get(url, params=params).text
            print(f'Если передать в параметре method значение {method_value}, то вернется {response}')
    else:
        print(f'Перебор с методом {method}:')
        print('---------------------------------------------------------------------------------------')
        for method_value in method_values:
            data = {
                "method": method_value
            }
            if method == 'post':
                response = requests.post(url, data=data).text
                print(f'Если передать в параметре method значение {method_value}, то вернется {response}')
            elif method == 'put':
                response = requests.put(url, data=data).text
                print(f'Если передать в параметре method значение {method_value}, то вернется {response}')
            else:
                response = requests.delete(url, data=data).text
                print(f'Если передать в параметре method значение {method_value}, то вернется {response}')

