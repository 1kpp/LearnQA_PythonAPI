import requests
import time

url = 'https://playground.learnqa.ru/ajax/api/longtime_job'
# Create job
response = requests.get(url).json()

# Request before job is ready
response_2 = requests.get(url, params={"token": response["token"]}).json()
assert response_2['status'] == 'Job is NOT ready'

# Wait till the job is ready
time.sleep(response['seconds'])

# Request after job is ready
response_3 = requests.get(url, params={"token": response["token"]}).json()
print(response_3)
assert response_3['status'] == 'Job is ready'
if 'result' in response_3:
    assert True
