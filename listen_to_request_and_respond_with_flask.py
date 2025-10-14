#!/usr/bin/env python3

import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
CORS(app)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(console_handler)

file_handler = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)


@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json()
    username = data.get("username", "Guest")

    logger.info(f"Received username: {username}")

    if not username.strip():
        logger.warning("Empty username received")
        return jsonify({"error": "Username cannot be empty."}), 400

    if username.lower() == "error":
        logger.error("Simulated crash triggered by username 'error'")
        raise Exception("Simulated server crash!")

    message = f"Hello, {username}!"
    logger.info(f"Returning message: {message}")

    return jsonify({"message": message})


@app.errorhandler(Exception)
def handle_exception(e):
    """Catch all exceptions so they’re also logged."""
    logger.exception("Unhandled exception occurred")
    return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
