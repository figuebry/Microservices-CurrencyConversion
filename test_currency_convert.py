import requests

data = {
    "amount": 100,
    "from_currency": "USD",
    "to_currency": "EUR"
}

response = requests.post(
    "http://localhost:5002/convert",
    json=data
)

print("Status Code:", response.status_code)
print("Response:", response.json())
