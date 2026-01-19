import requests

TOKEN = "8214376499:AAG7tJAD5A-Ur9jks0XgKajxMXOotVK3ZWE"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

response = requests.get(url).json()
print(response)