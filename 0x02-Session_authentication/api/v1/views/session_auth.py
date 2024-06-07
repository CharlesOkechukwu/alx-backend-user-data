#!/usr/bin/env python3
"""module for implementing session login"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login/', methods=['POST'],
                 strict_slashes=False)
def login() -> str:
    """return a User object based on email and password"""
    email = request.form.get('email')
    password = request.form.get('passowrd')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if user is None or user == []:
        return jsonify({'error': 'no user found for this email'}), 404
    if not user[0].is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    session_name = os.getenv('SESSION_NAME')
    response = jsonify(user[0].to_json())
    if session_name is not None and session_id:
        response.set_cookie(session_name, session_id)
    return response
