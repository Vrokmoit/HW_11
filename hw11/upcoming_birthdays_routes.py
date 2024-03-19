import requests

# URL маршруту для отримання списку контактів з днями народження в найближчі 7 днів
url = "http://127.0.0.1:8000/contacts/birthdays/"

# Виконання запиту GET
response = requests.get(url)

# Перевірка статусу відповіді
if response.status_code == 200:
    # Результат успішний, виведемо дані контактів
    contacts = response.json()
    print("Список контактів з днями народження в найближчі 7 днів:")
    for contact in contacts:
        print(contact)
else:
    # Відображення повідомлення про помилку
    print(f"Помилка: {response.status_code}")
