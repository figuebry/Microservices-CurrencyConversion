
from flask import Flask, request, jsonify

app = Flask(__name__)

exchange_rates = {
    ("USD", "EUR"): 0.92,
    ("EUR", "USD"): 1.09,
    ("USD", "GBP"): 0.79,
    ("GBP", "USD"): 1.27,
    ("USD", "CAD"): 1.40,
    ("CAD", "USD"): 0.71
}


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

    conversion = (from_currency.upper(), to_currency.upper())

    if conversion not in exchange_rates:
        return jsonify({
            "status": "error",
            "message": "Currency conversion not supported"
        }), 400

    converted_amount = amount * exchange_rates[conversion]

    return jsonify({
        "status": "success",
        "original_amount": amount,
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "exchange_rate": exchange_rates[conversion],
        "converted_amount": round(converted_amount, 2)
    })


if __name__ == "__main__":
    app.run(port=5002, debug=True)
