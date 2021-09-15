import requests

url = 'https://playground.learnqa.ru/api/long_redirect'
response = requests.get(url)

count_of_urls = len(response.history)
final_url = response.url
print(f'Общее количество переходов - {count_of_urls}. Количество переходов от начальной точке - {count_of_urls - 1}')
print(f'Итоговый урл -  {final_url}')