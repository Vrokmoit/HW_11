import requests

url = "http://127.0.0.1:8000/contacts/10"  
data = {
    "first_name": "ДFDFDа",
    "last_name": "FDFFDFDF",
    "email": "-",
    "phone_number": "+2323434432",
    "birthday": "2001-03-19",
    "additional_data": "" 
}

response = requests.put(url, json=data)

print(response.status_code)
print(response.json())
