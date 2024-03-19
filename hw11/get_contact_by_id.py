import requests

url = 'http://localhost:8000/contacts/10'
response = requests.get(url)

if response.status_code == 200:
    print(response.json())  # Вивести відповідь у форматі JSON
else:
    print(f"Статус код: {response.status_code}. Контакт не знайдено.")
