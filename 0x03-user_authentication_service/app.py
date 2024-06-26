#!/usr/bin/env python3
"""Flask app module"""
from flask import Flask, jsonify, request
from flask import abort, make_response, redirect
from auth import Auth


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


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """validate a user's credentials for log in and create a session
    if login was successful"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    resp = make_response(
        jsonify({"email": "{}".format(email), "message": "logged in"}))
    resp.set_cookie("session_id", AUTH.create_session(email))
    return resp


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout() -> None:
    """log out a user and delete session"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", strict_slashes=False)
def profile() -> None:
    """Handle profile request"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": "{}".format(user.email)}), 200


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """generate and return reset password token"""
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({
        "email": '{}'.format(email),
        "reset_token": "{}".format(reset_token)}), 200


@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password():
    """update password using new reset token"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)
    return jsonify({"email": "{}".format(email),
                    "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
