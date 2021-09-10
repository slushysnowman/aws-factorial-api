from flask import Flask, request, jsonify
from math import factorial

app = Flask(__name__)


@app.route("/api/v1/factorial", methods=["GET"])
def return_factorial():
    if "number" in request.args:
        try:
            number = int(request.args["number"])
            return jsonify(factorial(number))
        except ValueError:
            return "Invalid value", 403
    return "Please supply number parameter", 403
