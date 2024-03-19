import requests

def delete_contact(contact_id):
    url = f"http://127.0.0.1:8000/contacts/{contact_id}"
    response = requests.delete(url)
    
    if response.status_code == 200:
        print("Контакт успішно видалено")
    elif response.status_code == 404:
        print("Контакт не знайдено")
    else:
        print("Помилка:", response.status_code)

delete_contact(8)
