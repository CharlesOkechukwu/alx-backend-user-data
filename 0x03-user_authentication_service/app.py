#!/usr/bin/env python3
"""Flask app module"""
from flask import Flask, jsonify, request
from .auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route("/")
def root() -> str:
    """index root"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
    """register a user route"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": "{}".format(email), "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
