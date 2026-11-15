from flask import Flask, request, jsonify
import requests # markeeta addded

app = Flask(__name__)


# markeeta addded
def get_exchange_rate(from_currency, to_currency):
    url = f"https://api.frankfurter.dev/v2/rate/{from_currency}/{to_currency}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        return response.json()["rate"]

    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
        return None


@app.route("/convert", methods=["POST"])
def convert_currency():

    data = request.get_json()

    amount = data.get("amount")
    from_currency = data.get("from_currency")
    to_currency = data.get("to_currency")

    if amount is None or not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
        return jsonify({
            "status": "error",
            "message": "A valid positive amount is required"
        }), 400

    if not from_currency or not to_currency:
        return jsonify({
            "status": "error",
            "message": "Both currencies are required"
        }), 400

    conversion = f"{from_currency.upper()}_{to_currency.upper()}"

    # markeeta addded
    current_rate = get_exchange_rate(from_currency.upper(), to_currency.upper())

    if current_rate is None:
        return jsonify({
            "status": "error",
            "message": "Unable to retrieve current exchange rate"
        }), 503

    converted_amount = amount * current_rate

    return jsonify({
        "status": "success",
        "original_amount": amount,
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "exchange_rate": current_rate,
        "converted_amount": round(converted_amount, 2)
    })


if __name__ == "__main__":
    app.run(port=5002, debug=True)