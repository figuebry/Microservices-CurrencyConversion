# Currency Converter Microservice

## Description

The Currency Converter microservice accepts an amount and two currency codes, then returns the converted amount using predefined exchange rates.

The service currently supports six conversions:

- USD to EUR
- EUR to USD
- USD to GBP
- GBP to USD
- USD to CAD
- CAD to USD

Exchange rates are hardcoded and are not updated automatically.

## Communication Contract

### Service Information

| Property | Value |
|---|---|
| Protocol | HTTP |
| Method | POST |
| Endpoint | `/convert` |
| Port | 5002 |
| Content-Type | application/json |

### 1. Requesting Data

To request a currency conversion, send an HTTP POST request to:

`http://localhost:5002/convert`

The request must contain the following JSON fields:

| Field | Data Type | Description |
|---|---|---|
| `amount` | Number | Amount to convert. Must be positive. |
| `from_currency` | String | Currency being converted from. |
| `to_currency` | String | Currency being converted to. |

**Example Request (Python):**

```python
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
```

### 2. Receiving Data

The microservice returns a JSON response containing the conversion results.

**Example Successful Response:**

```json
{
    "status": "success",
    "original_amount": 100,
    "from_currency": "USD",
    "to_currency": "EUR",
    "exchange_rate": 0.92,
    "converted_amount": 92.0
}
```

To retrieve the returned information, the requesting application can use:

```python
result = response.json()

if response.status_code == 200:
    converted_amount = result["converted_amount"]
    print(converted_amount)
else:
    print(result["message"])
```

### 3. Error Handling

The microservice returns HTTP 400 when a request contains invalid or unsupported information.

Possible error responses include:

**Missing or invalid amount:**

```json
{
    "status": "error",
    "message": "A valid positive amount is required"
}
```

**Missing currency information:**

```json
{
    "status": "error",
    "message": "Both currencies are required"
}
```

**Unsupported conversion:**

```json
{
    "status": "error",
    "message": "Currency conversion not supported"
}
```

## UML Sequence Diagram

The following diagram illustrates how a requesting application communicates with the Currency Converter microservice.

## Running the Microservice

Install Flask if it is not already installed:

```bash
pip install flask
```

Start the microservice:

```bash
python currency_convert.py
```

The service will run locally on port `5002`.


## Dependencies

- Python 3
- Flask
- Requests (required by applications communicating with this service, not by the microservice itself)