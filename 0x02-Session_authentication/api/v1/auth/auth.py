#!/usr/bin/env python3
"""module to implement auth class"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """class managing API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check path to confirm authentication requirement"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        for route in excluded_paths:
            if route.endswith('*') and path.startswith(route[:-1]):
                return False
            elif path == route or path + '/' == route:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """check the authorization header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> str:
        """handle the current user"""
        return None

    def session_cookie(self, request=None) -> str:
        """return session cookie value from a request"""
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)
