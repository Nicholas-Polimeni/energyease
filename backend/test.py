import requests


data = {"message": "Hello, World!"}

response = requests.get(url, json=data)
print(response.request.url)
print(response)
