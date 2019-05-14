import requests

response = requests.post("http://127.0.0.1:8000/api/auth",
                         json={"login": "admin", "password": "password"})
print(response.json())
token = response.json()["token"]
print(requests.get(f"http://127.0.0.1:8000/api/task?token={token}").json())