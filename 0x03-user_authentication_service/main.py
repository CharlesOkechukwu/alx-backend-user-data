#!/usr/bin/env python3
"""Perform integration testing"""
import requests


localhost = "http://0.0.0.0:5000/{}"


def register_user(email: str, password: str) -> None:
    """test the user registration endpoint"""
    url = localhost.format("users")
    payload = {"email": email, "password": password}
    response = {'email': email, 'message': 'user created'}
    resp = requests.post(url, data=payload)
    assert resp.json() == response

    response = {'message': 'email already registered'}
    resp = requests.post(url, data=payload)
    assert resp.json == response
    assert resp.status_code == 400


def log_in_wrong_password(email: str, password: str) -> None:
    """test wrong login password"""
    url = localhost.format("sessions")
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 401
    assert response.cookies == {}


def log_in(email: str, password: str) -> str:
    """test the login endpoint"""
    url = localhost.format("sessions")
    payload = {"email": email, "password": password}
    message = {"email": email, "message": "logged in"}
    response = requests.post(url, data=payload)
    assert response.status_code == 200
    assert response.json() == message
    assert response.cookies.get("session_id") is not None
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """test the profile endpoint"""
    url = localhost.format("profile")
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """test logged in profile end point"""
    url = localhost.format("profile")
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    assert response.json().get('email') is not None


def log_out(session_id: str) -> None:
    """test user log out endpoint"""
    url = localhost.format("sessions")
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}
    assert response.cookies.get("session_id") is None


def reset_password_token(email: str) -> str:
    """test the reset password token endpoint"""
    url = localhost.format("reset_password")
    payload = {"email": email}
    response = requests.post(url, data=payload)
    assert response.status_code == 200
    assert response.json().get('email') == email
    assert response.json().get('reset_token') is not None
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test the update password endpoint"""
    url = localhost.format("reset_password")
    payload = {
        "email": email, "reset_token": reset_token,
        "new_password": new_password}
    message = {"email": email, "message": "Password updated"}
    response = requests.put(url, data=payload)
    assert response.status_code == 200
    assert response.json() == message


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
