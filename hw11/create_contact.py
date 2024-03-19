import requests

url = "http://127.0.0.1:8000/contacts/"

data = {
    "first_name": "ЫААВАВАt",
    "last_name": "АВАВАВАВА",
    "email": "ffffff@gmail.com",
    "phone_number": "+380112345032",
    "birthday": "2004-01-06",
    "additional_data": "БЕБЕБЕБЕБЕБЕБЕБЕБЕ"  
}


# Відправлення POST-запиту на сервер
response = requests.post(url, json=data)

# Перевірка статусу відповіді
if response.status_code == 200:
    print("Контакт успішно створено:", response.json())
else:
    print("Виникла помилка:", response.status_code)
    print("Текст помилки:", response.text)
