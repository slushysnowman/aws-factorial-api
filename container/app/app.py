from flask import Flask, request, jsonify
from math import factorial

app = Flask(__name__)


@app.route("/api/v1/factorial", methods=["GET"])
def return_factorial():
    if "number" in request.args:
        try:
            number = int(request.args["number"])
            answer = {"factorial": factorial(number)}
            return jsonify(answer)
        except ValueError:
            return "Invalid value", 400
    return "Please supply number parameter", 400
