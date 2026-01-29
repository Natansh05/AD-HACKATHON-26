import requests

LOGIN_URL = "http://13.234.226.222/api/auth/login/"

def login(username: str, password: str):
    payload = {
        "username": username,
        "password": password
    }

    response = requests.post(
        LOGIN_URL,
        json=payload,
        timeout=10
    )

    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json()
